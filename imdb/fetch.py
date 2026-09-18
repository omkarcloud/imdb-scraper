"""IMDB transport: plain HTTP via curl_cffi, no browser.

Validated 2026-08-25: api.graphql.imdb.com answers arbitrary (non-persisted)
GraphQL queries over plain curl_cffi with no cookies and no auth — the
x-imdb-client-name header plus imdb.com origin/referer are all it wants.
Only the www.imdb.com HTML pages sit behind AWS WAF (202 challenge with an
x-amzn-waf-action header); we never touch them. Autocomplete rides the
separate v3.sg.media-imdb.com suggestion API, also cookie-free.

Stress-tested 2026-08-25: 100 sequential TitleDetails queries from one
residential IP — 100/100 OK, zero blocks/429s, p50 0.65s p90 1.11s. No
rate limiting observed at that volume; IMDB_PROXY stays unset at launch.

Localization: the x-imdb-user-country header localizes release dates,
certificates and regional titles per request (x-imdb-user-language stays
en-US so text fields keep English). Full schema introspection is blocked
upstream, but per-type `__type(name:)` introspection works — that is how the
queries in imdb/queries.py were pinned.

FALLBACK HOOK: if direct requests AND config.IMDB_PROXY both start failing
with ImdbBlocked (WAF challenge/403/429/non-JSON), escalate the same way
etsy/fetch.py does — an ad-hoc patchright page-load on https://www.imdb.com/
to mint the aws-waf-token cookie, replayed by these curl sessions (sticky
proxy shared by browser and curl; see booking's property-page pattern). If
IMDB instead locks GraphQL down to persisted queries, re-sniff the site's
POSTs for operation hashes (TripAdvisor workflow). Not built now: dead code
while plain HTTP works cookie-free.
"""
import json
import os
import threading
import time
from urllib.parse import quote

import config

GRAPHQL_URL = "https://api.graphql.imdb.com/"
SUGGESTION_URL = "https://v3.sg.media-imdb.com/suggestion/x/{query}.json"
TIMEOUT = 10          # suggestion API answers in <1s
GRAPHQL_TIMEOUT = 25  # chart queries return ~200KB
IMPERSONATE = "chrome"


class ImdbUpstreamError(Exception):
    """Transport failure or 5xx — retryable."""


class ImdbBlocked(ImdbUpstreamError):
    """WAF challenge/403/429/non-JSON — retryable, and the patchright-fallback trigger."""


class ImdbBadRequest(Exception):
    """Upstream 400 / GraphQL validation error (bad params) — never retried."""


class ImdbNotFound(Exception):
    """Entity doesn't exist (null title/name for a well-formed id) — never retried."""


# One session per cheroot worker thread: a curl handle must not be shared
# across threads, but these calls are stateless so thread-lifetime sessions
# with keep-alive are enough.
_local = threading.local()


def _session():
    sess = getattr(_local, "session", None)
    if sess is None:
        from curl_cffi import requests as curl_requests
        sess = curl_requests.Session(impersonate=IMPERSONATE)
        if config.IMDB_PROXY:
            sess.proxies = {"http": config.IMDB_PROXY,
                            "https": config.IMDB_PROXY}
        _local.session = sess
    return sess


def _drop_session():
    """Close the thread's session so a poisoned keep-alive connection dies."""
    sess = getattr(_local, "session", None)
    _local.session = None
    if sess is not None:
        try:
            sess.close()
        except Exception:
            pass


def dump_debug(name, text):
    """Write raw response text to $IMDB_DEBUG_DIR/<name>.txt for post-mortems."""
    dbg = os.environ.get("IMDB_DEBUG_DIR", "")
    if dbg and text:
        try:
            os.makedirs(dbg, exist_ok=True)
            with open(os.path.join(dbg, name + ".txt"), "w") as f:
                f.write(text)
        except OSError:
            pass


def _graphql_headers(country):
    return {
        "content-type": "application/json",
        "x-imdb-client-name": "imdb-web-next-localized",
        "x-imdb-user-country": country,
        "x-imdb-user-language": "en-US",
        "origin": "https://www.imdb.com",
        "referer": "https://www.imdb.com/",
    }


def _classify(resp, host):
    """Map an HTTP response to the error taxonomy; return the JSON payload."""
    if resp.status_code == 400:
        raise ImdbBadRequest(resp.text[:200])
    if resp.status_code == 202 and resp.headers.get("x-amzn-waf-action"):
        dump_debug(f"waf_{host}", resp.text)
        raise ImdbBlocked(f"AWS WAF challenge from {host}")
    if resp.status_code in (403, 429, 503):
        dump_debug(f"blocked_{host}", resp.text)
        raise ImdbBlocked(f"HTTP {resp.status_code} from {host}")
    if resp.status_code != 200:
        raise ImdbUpstreamError(f"HTTP {resp.status_code} from {host}")
    try:
        return resp.json()
    except Exception:
        dump_debug(f"nonjson_{host}", resp.text)
        raise ImdbBlocked(f"non-JSON response from {host}")


def _graphql_once(query, variables, country):
    try:
        resp = _session().post(GRAPHQL_URL,
                               json={"query": query, "variables": variables},
                               headers=_graphql_headers(country),
                               timeout=GRAPHQL_TIMEOUT)
    except Exception as e:
        raise ImdbUpstreamError(f"request failed: {type(e).__name__}: {e}")

    payload = _classify(resp, "api.graphql.imdb.com")
    errors = payload.get("errors")
    if errors:
        # GraphQL-level errors on a 200: validation/parse problems are our
        # bug or bad user input — never retryable.
        msg = json.dumps(errors)[:300]
        raise ImdbBadRequest(f"graphql errors: {msg}")
    if not isinstance(payload.get("data"), dict):
        dump_debug("unexpected_graphql", resp.text)
        raise ImdbBlocked("unexpected GraphQL payload shape (no data)")
    return payload["data"]


def fetch_graphql(query, variables, *, country="US"):
    """POST one GraphQL query; return the `data` dict.

    Retries only ImdbUpstreamError (transport/5xx/block); ImdbBadRequest
    surfaces immediately — retrying bad params can never succeed."""
    return _retrying(lambda: _graphql_once(query, variables, country))


def _suggestions_once(query):
    url = SUGGESTION_URL.format(query=quote(query, safe=""))
    try:
        resp = _session().get(url, headers={"Accept": "application/json"},
                              timeout=TIMEOUT)
    except Exception as e:
        raise ImdbUpstreamError(f"request failed: {type(e).__name__}: {e}")

    payload = _classify(resp, "v3.sg.media-imdb.com")
    if not isinstance(payload.get("d"), list):
        # An unknown query returns {"q": ..., "v": 1} with no "d" — treat as
        # empty, not an error.
        if isinstance(payload, dict) and "q" in payload:
            return {"d": [], "q": payload.get("q")}
        dump_debug("unexpected_suggestion", resp.text)
        raise ImdbBlocked("unexpected suggestion payload shape")
    return payload


def fetch_suggestions(query):
    """GET the typeahead suggestion payload for `query` (not GraphQL)."""
    return _retrying(lambda: _suggestions_once(query))


def _retrying(fn):
    """Run fn() under the shared retry policy (ImdbUpstreamError only)."""
    last = None
    for attempt in range(1, config.MAX_RETRIES + 1):
        try:
            return fn()
        except ImdbUpstreamError as e:
            last = e
            _drop_session()
            if attempt < config.MAX_RETRIES:
                time.sleep(config.RETRY_BACKOFF * attempt)
    raise last

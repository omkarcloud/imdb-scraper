"""The 13 IMDb endpoints. Every path is served with and without the `/imdb`
prefix, so code generated against the hosted API on RapidAPI (paths like
/title/details) runs unchanged against this server."""
import json

from bottle import request, response, route

from imdb.autocomplete import autocomplete
from imdb.charts import CHART_KINDS, get_chart
from imdb.fetch import ImdbBadRequest, ImdbNotFound
from imdb.person import get_person_details
from imdb.search import search_titles
from imdb.title import (get_title_cast, get_title_details, get_title_episodes,
                        get_title_reviews)


def json_response(data, status=200):
    response.status = status
    response.content_type = "application/json"
    return json.dumps(data, ensure_ascii=False)


def q(name):
    """One query param as unicode (bottle 0.12's .get() hands back latin-1
    decoded bytes, so a UTF-8 "Amélie" would arrive as "AmÃ©lie")."""
    value = request.query.getunicode(name)
    return value.strip() if value else None


def call(label, fn, not_found=None):
    """Shared error mapping: bad params -> 400, missing entity -> 404,
    transport/blocks -> 500."""
    try:
        return json_response(fn())
    except ValueError as e:                # bad id / params
        return json_response({"error": str(e)}, 400)
    except ImdbBadRequest as e:            # upstream rejected the request
        return json_response({"error": f"imdb rejected the request: {e}"}, 400)
    except ImdbNotFound:
        return json_response({"error": not_found or "not found"}, 404)
    except Exception as e:                 # retries exhausted / blocked
        return json_response({"error": f"imdb {label} failed: {e}"}, 500)


def required(name):
    """(value, error_response) — the error is None when the param is there."""
    value = q(name)
    if not value:
        return None, json_response({"error": f"Missing required parameter: {name}"}, 400)
    return value, None


def mount(path, handler):
    """Serve a handler at /path and /imdb/path."""
    handler.__name__ = "imdb_" + path.strip("/").replace("/", "_").replace("-", "_")
    route(path, method="GET")(handler)
    route("/imdb" + path, method="GET")(handler)


def autocomplete_route():
    query, err = required("query")
    return err or call("autocomplete", lambda: autocomplete(query, q("country")))


def search_route():
    return call("search", lambda: search_titles(
        query=q("query"), title_type=q("type"), genre=q("genre"),
        start_year=q("start_year"), end_year=q("end_year"), sort=q("sort"),
        cursor=q("cursor"), country=q("country")))


def title_details_route():
    title, err = required("title_id")
    return err or call("title/details", lambda: get_title_details(title, q("country")),
                       not_found=f"title not found: {title}")


def title_cast_route():
    title, err = required("title_id")
    return err or call("title/cast", lambda: get_title_cast(title, cursor=q("cursor"), country=q("country")),
                       not_found=f"title not found: {title}")


def title_reviews_route():
    title, err = required("title_id")
    if err:
        return err
    include_spoilers = (q("include_spoilers") or "").lower() not in ("false", "0", "no")
    return call("title/reviews", lambda: get_title_reviews(
        title, sort=q("sort"), include_spoilers=include_spoilers,
        cursor=q("cursor"), country=q("country")),
        not_found=f"title not found: {title}")


def title_episodes_route():
    title, err = required("title_id")
    return err or call("title/episodes", lambda: get_title_episodes(
        title, season=q("season"), cursor=q("cursor"), country=q("country")),
        not_found=f"title not found: {title}")


def person_details_route():
    person, err = required("person_id")
    return err or call("person/details", lambda: get_person_details(person, q("country")),
                       not_found=f"person not found: {person}")


def chart_route(kind):
    def handler():
        return call(f"charts/{kind}", lambda: get_chart(kind, q("country")))
    return handler


ENDPOINTS = [
    ("/title/details", title_details_route),
    ("/search", search_route),
    ("/autocomplete", autocomplete_route),
    ("/title/cast", title_cast_route),
    ("/title/reviews", title_reviews_route),
    ("/title/episodes", title_episodes_route),
    ("/person/details", person_details_route),
] + [(f"/charts/{kind}", chart_route(kind)) for kind in CHART_KINDS]

for _path, _handler in ENDPOINTS:
    mount(_path, _handler)


@route("/", method="GET")
@route("/health", method="GET")
def health():
    return json_response({"status": "ok", "endpoints": [p for p, _ in ENDPOINTS]})

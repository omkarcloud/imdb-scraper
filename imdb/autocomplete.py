"""IMDB typeahead autocomplete (titles + people mixed).

Rides the v3.sg.media-imdb.com suggestion API — cookie-free plain HTTP, not
GraphQL. `country` is accepted for API uniformity but the suggestion API is
not localized, so it does not change results.

Smoke test (plain HTTP, no chrome pools, ONLY_SCRAPER not required):

    python imdb/autocomplete.py [query]
    python imdb/autocomplete.py "shawshank"
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from imdb import parsers, queries  # noqa: E402
from imdb import fetch  # noqa: E402  (module import so tests can monkeypatch)


def autocomplete(query, country=None):
    """Title/person suggestions for a partial query.

    Raises ValueError for bad input, fetch.ImdbUpstreamError for upstream
    failures."""
    query = (query or "").strip()
    if not query:
        raise ValueError("query is required")
    queries.normalize_country(country)  # validate even though unused

    payload = fetch.fetch_suggestions(query)
    results = parsers.parse_suggestions(payload)
    return {
        "query": query,
        "count": len(results),
        "results": results,
    }


if __name__ == "__main__":
    arg_query = sys.argv[1] if len(sys.argv) > 1 else "shawshank"
    out = autocomplete(arg_query)
    print(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"count={out['count']}", file=sys.stderr)

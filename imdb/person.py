"""IMDB person (name) details: bio + known-for + filmography in one call.

`person_id` accepts a bare nm-id or any imdb.com /name/ URL.

Smoke test (plain HTTP, no chrome pools, ONLY_SCRAPER not required):

    python imdb/person.py [person_id]
    python imdb/person.py nm0000138
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from imdb import parsers, queries  # noqa: E402
from imdb import fetch  # noqa: E402  (module import so tests can monkeypatch)


def get_person_details(person_id, country=None):
    """Consolidated details for one person.

    Raises ValueError for bad input, fetch.ImdbNotFound for a nonexistent id,
    fetch.ImdbUpstreamError for upstream failures."""
    person_id = queries.normalize_person_id(person_id)
    country = queries.normalize_country(country)

    data = fetch.fetch_graphql(queries.PERSON_DETAILS, {"id": person_id},
                               country=country)
    result = parsers.parse_person(data)
    if result is None:
        raise fetch.ImdbNotFound(f"person not found: {person_id}")
    result["country"] = country
    return result


if __name__ == "__main__":
    arg_id = sys.argv[1] if len(sys.argv) > 1 else "nm0000138"
    out = get_person_details(arg_id)
    print(json.dumps(out, indent=2, ensure_ascii=False))

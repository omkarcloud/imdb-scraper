"""IMDB title search (advancedTitleSearch) with filters + cursor pagination.

At least one of query / type / genre / start_year / end_year must be given
(a bare unconstrained search of 11M titles is never what the caller meant).

Smoke test (plain HTTP, no chrome pools, ONLY_SCRAPER not required):

    python imdb/search.py [query]
    python imdb/search.py matrix
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from imdb import parsers, queries  # noqa: E402
from imdb import fetch  # noqa: E402  (module import so tests can monkeypatch)

PAGE_SIZE = 50
MIN_YEAR, MAX_YEAR = 1874, 2100  # IMDB's oldest title is from 1874


def _year(name, value):
    if value in (None, ""):
        return None
    try:
        value = int(value)
        if not MIN_YEAR <= value <= MAX_YEAR:
            raise ValueError
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be an integer {MIN_YEAR}-{MAX_YEAR}")
    return value


def search_titles(query=None, title_type=None, genre=None, start_year=None,
                  end_year=None, sort=None, cursor=None, country=None):
    """One page of title search results (50 per page, cursor-paginated).

    Raises ValueError for bad input, fetch.ImdbUpstreamError for upstream
    failures."""
    query = (query or "").strip()
    country = queries.normalize_country(country)
    sort = (sort or "popularity").strip().lower()
    if sort not in queries.SEARCH_SORTS:
        raise ValueError(
            f"sort must be one of {', '.join(sorted(queries.SEARCH_SORTS))}, got: {sort!r}")

    constraints = {}
    if query:
        constraints["titleTextConstraint"] = {"searchTerm": query}

    if title_type not in (None, ""):
        title_type = str(title_type).strip().lower()
        if title_type not in queries.TITLE_TYPE_IDS:
            raise ValueError(
                f"type must be one of {', '.join(sorted(queries.TITLE_TYPE_IDS))}, got: {title_type!r}")
        constraints["titleTypeConstraint"] = {
            "anyTitleTypeIds": queries.TITLE_TYPE_IDS[title_type]}
    else:
        title_type = None

    if genre not in (None, ""):
        genre = str(genre).strip()
        matched = next((g for g in queries.GENRES if g.lower() == genre.lower()), None)
        if not matched:
            raise ValueError(
                f"genre must be one of {', '.join(queries.GENRES)}, got: {genre!r}")
        genre = matched
        constraints["genreConstraint"] = {"allGenreIds": [matched]}
    else:
        genre = None

    start_year = _year("start_year", start_year)
    end_year = _year("end_year", end_year)
    if start_year and end_year and start_year > end_year:
        raise ValueError("start_year must not be after end_year")
    if start_year or end_year:
        date_range = {}
        if start_year:
            date_range["start"] = f"{start_year}-01-01"
        if end_year:
            date_range["end"] = f"{end_year}-12-31"
        constraints["releaseDateConstraint"] = {"releaseDateRange": date_range}

    if not constraints:
        raise ValueError(
            "at least one of query, type, genre, start_year, end_year is required")

    variables = {"first": PAGE_SIZE, "constraints": constraints,
                 "sort": queries.SEARCH_SORTS[sort]}
    if cursor:
        variables["after"] = cursor
    data = fetch.fetch_graphql(queries.SEARCH_TITLES, variables, country=country)
    results, pagination = parsers.parse_search(data)
    return {
        "query": query or None,
        "type": title_type,
        "genre": genre,
        "start_year": start_year,
        "end_year": end_year,
        "sort": sort,
        "country": country,
        "count": len(results),
        "pagination": pagination,
        "results": results,
    }


if __name__ == "__main__":
    arg_query = sys.argv[1] if len(sys.argv) > 1 else "matrix"
    out = search_titles(arg_query)
    print(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"count={out['count']} total={out['pagination']['total']}", file=sys.stderr)

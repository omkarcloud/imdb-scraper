"""IMDB title endpoints: details, cast, reviews, episodes.

All GraphQL over plain curl_cffi (imdb/fetch.py). `title_id` accepts a bare
tt-id or any imdb.com /title/ URL. Cursors are the opaque GraphQL pageInfo
cursors passed back verbatim as `pagination.next_cursor`; helpfulness-sorted
review cursors can drift as vote counts move — `newest` is the stable walk.

Smoke test (plain HTTP, no chrome pools, ONLY_SCRAPER not required):

    python imdb/title.py details tt0111161
    python imdb/title.py details tt0944947            # TV: seasons block
    python imdb/title.py cast tt0944947
    python imdb/title.py reviews tt1375666 newest
    python imdb/title.py episodes tt0944947           # seasons list
    python imdb/title.py episodes tt0944947 1         # season 1 episodes
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from imdb import parsers, queries  # noqa: E402
from imdb import fetch  # noqa: E402  (module import so tests can monkeypatch)

CAST_PAGE_SIZE = 50
REVIEWS_PAGE_SIZE = 25
EPISODES_PAGE_SIZE = 50
MAX_SEASON = 1000


def get_title_details(title_id, country=None):
    """Consolidated one-call details for a movie/show.

    Raises ValueError for bad input, fetch.ImdbNotFound for a nonexistent id,
    fetch.ImdbUpstreamError for upstream failures."""
    title_id = queries.normalize_title_id(title_id)
    country = queries.normalize_country(country)

    data = fetch.fetch_graphql(queries.TITLE_DETAILS, {"id": title_id},
                               country=country)
    result = parsers.parse_title_details(data)
    if result is None:
        raise fetch.ImdbNotFound(f"title not found: {title_id}")
    result["country"] = country
    return result


def get_title_cast(title_id, cursor=None, country=None):
    """One page of full cast credits (50 per page, cursor-paginated)."""
    title_id = queries.normalize_title_id(title_id)
    country = queries.normalize_country(country)

    variables = {"id": title_id, "first": CAST_PAGE_SIZE}
    if cursor:
        variables["after"] = cursor
    data = fetch.fetch_graphql(queries.TITLE_CAST, variables, country=country)
    parsed = parsers.parse_cast(data)
    if parsed is None:
        raise fetch.ImdbNotFound(f"title not found: {title_id}")
    header, cast, pagination = parsed
    return {
        **header,
        "country": country,
        "count": len(cast),
        "pagination": pagination,
        "results": cast,
    }


def get_title_reviews(title_id, sort="helpfulness", include_spoilers=True,
                      cursor=None, country=None):
    """One page of user reviews (25 per page, cursor-paginated)."""
    title_id = queries.normalize_title_id(title_id)
    country = queries.normalize_country(country)
    sort = (sort or "helpfulness").strip().lower()
    if sort not in queries.REVIEW_SORTS:
        raise ValueError(
            f"sort must be one of {', '.join(sorted(queries.REVIEW_SORTS))}, got: {sort!r}")

    variables = {"id": title_id, "first": REVIEWS_PAGE_SIZE,
                 "sort": queries.REVIEW_SORTS[sort]}
    if not include_spoilers:
        variables["filter"] = {"spoiler": "EXCLUDE"}
    if cursor:
        variables["after"] = cursor
    data = fetch.fetch_graphql(queries.TITLE_REVIEWS, variables, country=country)
    parsed = parsers.parse_reviews(data)
    if parsed is None:
        raise fetch.ImdbNotFound(f"title not found: {title_id}")
    header, reviews, pagination = parsed
    return {
        **header,
        "country": country,
        "sort": sort,
        "includes_spoilers": bool(include_spoilers),
        "count": len(reviews),
        "pagination": pagination,
        "results": reviews,
    }


def get_title_episodes(title_id, season=None, cursor=None, country=None):
    """Episodes of one season (50 per page), or the seasons list when
    `season` is omitted. Unaired specials ride along as episode 0."""
    title_id = queries.normalize_title_id(title_id)
    country = queries.normalize_country(country)

    if season in (None, ""):
        data = fetch.fetch_graphql(queries.TITLE_SEASONS, {"id": title_id},
                                   country=country)
        result = parsers.parse_seasons(data)
        if result is None:
            raise fetch.ImdbNotFound(f"title not found: {title_id}")
        result["country"] = country
        return result

    try:
        season = int(season)
        if not 1 <= season <= MAX_SEASON:
            raise ValueError
    except (TypeError, ValueError):
        raise ValueError(f"season must be an integer 1-{MAX_SEASON}")

    variables = {"id": title_id, "first": EPISODES_PAGE_SIZE,
                 "filter": {"includeSeasons": [str(season)]}}
    if cursor:
        variables["after"] = cursor
    data = fetch.fetch_graphql(queries.TITLE_EPISODES, variables, country=country)
    parsed = parsers.parse_episodes(data)
    if parsed is None:
        raise fetch.ImdbNotFound(f"title not found: {title_id}")
    header, episodes, pagination = parsed
    return {
        **header,
        "country": country,
        "season": season,
        "count": len(episodes),
        "pagination": pagination,
        "results": episodes,
    }


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else "details"
    arg_id = sys.argv[2] if len(sys.argv) > 2 else "tt0111161"
    extra = sys.argv[3] if len(sys.argv) > 3 else None
    if command == "details":
        out = get_title_details(arg_id)
    elif command == "cast":
        out = get_title_cast(arg_id, cursor=extra)
    elif command == "reviews":
        out = get_title_reviews(arg_id, sort=extra or "helpfulness")
    elif command == "episodes":
        out = get_title_episodes(arg_id, season=extra)
    else:
        raise SystemExit(f"unknown command: {command}")
    print(json.dumps(out, indent=2, ensure_ascii=False))

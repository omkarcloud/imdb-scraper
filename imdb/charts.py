"""IMDB charts: Top 250s, MovieMeter/TVMeter, weekend box office, StarMeter.

Single-shot lists (no cursor params on the public endpoints — the whole
chart comes back in one call): top-movies / top-tv return the full 250,
popular-movies / popular-tv the top 100, popular-celebrities the top 100.

Smoke test (plain HTTP, no chrome pools, ONLY_SCRAPER not required):

    python imdb/charts.py [chart]
    python imdb/charts.py top-movies
    python imdb/charts.py box-office
    python imdb/charts.py popular-celebrities
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from imdb import parsers, queries  # noqa: E402
from imdb import fetch  # noqa: E402  (module import so tests can monkeypatch)

TOP_CHART_SIZE = 250      # TOP_RATED_* charts are exactly 250 titles
POPULAR_CHART_SIZE = 100  # MovieMeter/TVMeter/StarMeter published depth

CHART_KINDS = sorted(queries.TITLE_CHARTS) + ["box-office", "popular-celebrities"]


def get_title_chart(kind, country=None):
    """One ranked title chart: top-movies, top-tv, popular-movies, popular-tv."""
    kind = (kind or "").strip().lower()
    if kind not in queries.TITLE_CHARTS:
        raise ValueError(
            f"chart must be one of {', '.join(sorted(queries.TITLE_CHARTS))}, got: {kind!r}")
    country = queries.normalize_country(country)

    first = TOP_CHART_SIZE if kind.startswith("top-") else POPULAR_CHART_SIZE
    data = fetch.fetch_graphql(
        queries.CHART_TITLES,
        {"first": first, "chartType": queries.TITLE_CHARTS[kind]},
        country=country)
    results, pagination = parsers.parse_chart_titles(data)
    return {
        "chart": kind,
        "country": country,
        "count": len(results),
        "pagination": pagination,
        "results": results,
    }


def get_box_office(country=None):
    """The weekend box office chart (US theatrical)."""
    country = queries.normalize_country(country)
    data = fetch.fetch_graphql(queries.BOX_OFFICE, {}, country=country)
    weekend, entries = parsers.parse_box_office(data)
    return {
        "chart": "box-office",
        "country": country,
        "weekend": weekend,
        "count": len(entries),
        "results": entries,
    }


def get_popular_celebrities(country=None):
    """The StarMeter chart: the 100 most popular people this week."""
    country = queries.normalize_country(country)
    data = fetch.fetch_graphql(queries.POPULAR_CELEBRITIES,
                               {"first": POPULAR_CHART_SIZE}, country=country)
    results, pagination = parsers.parse_chart_names(data)
    return {
        "chart": "popular-celebrities",
        "country": country,
        "count": len(results),
        "pagination": pagination,
        "results": results,
    }


def get_chart(kind, country=None):
    """Dispatch any chart kind (routes layer entry point)."""
    kind_clean = (kind or "").strip().lower()
    if kind_clean == "box-office":
        return get_box_office(country)
    if kind_clean == "popular-celebrities":
        return get_popular_celebrities(country)
    return get_title_chart(kind_clean, country)


if __name__ == "__main__":
    arg_kind = sys.argv[1] if len(sys.argv) > 1 else "top-movies"
    out = get_chart(arg_kind)
    print(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"chart={out['chart']} count={out['count']}", file=sys.stderr)

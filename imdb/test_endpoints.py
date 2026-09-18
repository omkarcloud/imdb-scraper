"""Offline tests for the imdb business modules (fetch layer monkeypatched).

    python -m pytest imdb/test_endpoints.py -q
"""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from imdb import fetch, queries  # noqa: E402
from imdb.autocomplete import autocomplete  # noqa: E402
from imdb.charts import get_chart  # noqa: E402
from imdb.person import get_person_details  # noqa: E402
from imdb.search import search_titles  # noqa: E402
from imdb.title import (get_title_cast, get_title_details,  # noqa: E402
                        get_title_episodes, get_title_reviews)

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


def _fixture(name):
    with open(os.path.join(FIXTURES, name)) as f:
        return json.load(f)


# ---- id / input normalization ----------------------------------------------

def test_normalize_title_id():
    assert queries.normalize_title_id("tt0111161") == "tt0111161"
    assert queries.normalize_title_id(" tt0111161 ") == "tt0111161"
    assert queries.normalize_title_id(
        "https://www.imdb.com/title/tt0111161/?ref_=hm") == "tt0111161"
    assert queries.normalize_title_id(
        "https://www.imdb.com/de/title/tt0111161/") == "tt0111161"
    for bad in ("", "0111161", "nm0000138", "https://www.imdb.com/name/nm0000138/"):
        with pytest.raises(ValueError):
            queries.normalize_title_id(bad)


def test_normalize_person_id():
    assert queries.normalize_person_id("nm0000138") == "nm0000138"
    assert queries.normalize_person_id(
        "https://www.imdb.com/name/nm0000138/bio/") == "nm0000138"
    for bad in ("", "tt0111161", "leonardo"):
        with pytest.raises(ValueError):
            queries.normalize_person_id(bad)


def test_normalize_country():
    assert queries.normalize_country(None) == "US"
    assert queries.normalize_country("") == "US"
    assert queries.normalize_country("in") == "IN"
    with pytest.raises(ValueError):
        queries.normalize_country("USA")


# ---- autocomplete -----------------------------------------------------------

def test_autocomplete(monkeypatch):
    calls = {}

    def fake_suggestions(query):
        calls["query"] = query
        return _fixture("suggestions_shawshank.json")

    monkeypatch.setattr(fetch, "fetch_suggestions", fake_suggestions)
    out = autocomplete(" shawshank ")
    assert calls == {"query": "shawshank"}
    assert out["query"] == "shawshank"
    assert out["count"] == len(out["results"]) > 0
    assert out["results"][0]["id"] == "tt0111161"


def test_autocomplete_rejects_bad_input():
    with pytest.raises(ValueError):
        autocomplete("")
    with pytest.raises(ValueError):
        autocomplete("dune", country="USA")


# ---- title details ----------------------------------------------------------

def test_title_details_envelope(monkeypatch):
    calls = {}

    def fake_graphql(query, variables, country="US"):
        calls["variables"], calls["country"] = variables, country
        return _fixture("title_details_movie.json")

    monkeypatch.setattr(fetch, "fetch_graphql", fake_graphql)
    out = get_title_details("https://www.imdb.com/title/tt0111161/", country="in")
    assert calls["variables"] == {"id": "tt0111161"}   # URL normalized to id
    assert calls["country"] == "IN"
    assert out["id"] == "tt0111161"
    assert out["country"] == "IN"


def test_title_details_not_found(monkeypatch):
    monkeypatch.setattr(fetch, "fetch_graphql",
                        lambda *a, **k: _fixture("title_details_missing_stub.json"))
    with pytest.raises(fetch.ImdbNotFound):
        get_title_details("tt9999999999")


# ---- cast / reviews / episodes ----------------------------------------------

def test_cast_envelope(monkeypatch):
    calls = {}

    def fake_graphql(query, variables, country="US"):
        calls["variables"] = variables
        return _fixture("title_cast_page1.json")

    monkeypatch.setattr(fetch, "fetch_graphql", fake_graphql)
    out = get_title_cast("tt0944947", cursor="CURSOR123")
    assert calls["variables"]["after"] == "CURSOR123"
    assert calls["variables"]["first"] == 50
    assert out["count"] == 50
    assert out["pagination"]["next_cursor"]
    assert out["results"][0]["name"] == "Peter Dinklage"


def test_reviews_envelope(monkeypatch):
    calls = {}

    def fake_graphql(query, variables, country="US"):
        calls["variables"] = variables
        return _fixture("title_reviews_page1.json")

    monkeypatch.setattr(fetch, "fetch_graphql", fake_graphql)
    out = get_title_reviews("tt1375666", sort="newest", include_spoilers=False)
    assert calls["variables"]["sort"] == {"by": "SUBMISSION_DATE", "order": "DESC"}
    assert calls["variables"]["filter"] == {"spoiler": "EXCLUDE"}
    assert out["sort"] == "newest"
    assert out["includes_spoilers"] is False
    assert out["count"] == 25

    with pytest.raises(ValueError):
        get_title_reviews("tt1375666", sort="bestest")


def test_episodes_branches(monkeypatch):
    def fake_graphql(query, variables, country="US"):
        if "filter" in variables:
            assert variables["filter"] == {"includeSeasons": ["1"]}
            return _fixture("title_episodes_s1.json")
        return _fixture("title_seasons.json")

    monkeypatch.setattr(fetch, "fetch_graphql", fake_graphql)
    seasons = get_title_episodes("tt0944947")
    assert seasons["seasons"]["count"] == 8
    episodes = get_title_episodes("tt0944947", season=1)
    assert episodes["season"] == 1
    assert episodes["count"] > 0

    with pytest.raises(ValueError):
        get_title_episodes("tt0944947", season="one")
    with pytest.raises(ValueError):
        get_title_episodes("tt0944947", season=0)


# ---- search -----------------------------------------------------------------

def test_search_constraints(monkeypatch):
    calls = {}

    def fake_graphql(query, variables, country="US"):
        calls["variables"] = variables
        return _fixture("search_page1.json")

    monkeypatch.setattr(fetch, "fetch_graphql", fake_graphql)
    out = search_titles("matrix", title_type="movie", genre="sci-fi",
                        start_year=1999, end_year=2003, sort="rating")
    constraints = calls["variables"]["constraints"]
    assert constraints["titleTextConstraint"] == {"searchTerm": "matrix"}
    assert constraints["titleTypeConstraint"] == {"anyTitleTypeIds": ["movie", "tvMovie"]}
    assert constraints["genreConstraint"] == {"allGenreIds": ["Sci-Fi"]}  # case-fixed
    assert constraints["releaseDateConstraint"] == {
        "releaseDateRange": {"start": "1999-01-01", "end": "2003-12-31"}}
    assert calls["variables"]["sort"] == {"sortBy": "USER_RATING", "sortOrder": "DESC"}
    assert out["genre"] == "Sci-Fi"
    assert out["count"] == 43                      # fixture has one full result page


def test_search_rejects_bad_input():
    with pytest.raises(ValueError):
        search_titles()                            # no constraints at all
    with pytest.raises(ValueError):
        search_titles("dune", title_type="podcast")
    with pytest.raises(ValueError):
        search_titles("dune", genre="Unknowncore")
    with pytest.raises(ValueError):
        search_titles("dune", start_year=2020, end_year=2010)
    with pytest.raises(ValueError):
        search_titles("dune", sort="best")


# ---- charts -----------------------------------------------------------------

def test_chart_dispatch(monkeypatch):
    calls = {}

    def fake_graphql(query, variables, country="US"):
        calls["variables"] = variables
        if "chartType" in variables:
            return _fixture("chart_top_movies_trimmed.json")
        if "first" in variables:
            return _fixture("chart_popular_celebrities_trimmed.json")
        return _fixture("chart_box_office.json")

    monkeypatch.setattr(fetch, "fetch_graphql", fake_graphql)

    out = get_chart("top-movies")
    assert calls["variables"] == {"first": 250, "chartType": "TOP_RATED_MOVIES"}
    assert out["chart"] == "top-movies"
    assert out["results"][0]["rank"] == 1

    out = get_chart("popular-tv")
    assert calls["variables"] == {"first": 100, "chartType": "MOST_POPULAR_TV_SHOWS"}

    out = get_chart("box-office")
    assert out["weekend"]["start_date"]
    assert out["results"][0]["weekend_gross"]["amount"] > 0

    out = get_chart("popular-celebrities")
    assert out["results"][0]["id"].startswith("nm")

    with pytest.raises(ValueError):
        get_chart("top-podcasts")


# ---- person -----------------------------------------------------------------

def test_person_envelope(monkeypatch):
    monkeypatch.setattr(fetch, "fetch_graphql",
                        lambda *a, **k: _fixture("person_details.json"))
    out = get_person_details("https://www.imdb.com/name/nm0000138/")
    assert out["id"] == "nm0000138"
    assert out["name"] == "Leonardo DiCaprio"
    assert out["country"] == "US"


def test_person_not_found(monkeypatch):
    monkeypatch.setattr(fetch, "fetch_graphql",
                        lambda *a, **k: {"name": {"id": "nm9999999999", "nameText": None}})
    with pytest.raises(fetch.ImdbNotFound):
        get_person_details("nm9999999999")

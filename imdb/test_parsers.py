"""Offline tests for the imdb parsers.

    python -m pytest imdb/test_parsers.py -q

Fixtures are real captures (2026-08-25) of api.graphql.imdb.com / the
v3.sg.media-imdb.com suggestion API, saved verbatim except the two chart
fixtures whose edge lists are trimmed to 5 rows to keep the repo light.
title_details_missing_stub.json is the nonexistent-id stub payload (IMDB
echoes {id, titleText: null, ...} instead of a null title). No network.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from imdb import parsers  # noqa: E402

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


def _fixture(name):
    with open(os.path.join(FIXTURES, name)) as f:
        return json.load(f)


MOVIE = _fixture("title_details_movie.json")
TV = _fixture("title_details_tv.json")
SPARSE = _fixture("title_details_sparse.json")
MISSING = _fixture("title_details_missing_stub.json")


# ---- autocomplete -----------------------------------------------------------

def test_suggestions():
    results = parsers.parse_suggestions(_fixture("suggestions_shawshank.json"))
    assert results
    top = results[0]
    assert top["id"] == "tt0111161"
    assert top["type"] == "movie"
    assert top["title"] == "The Shawshank Redemption"
    assert top["link"] == "https://www.imdb.com/title/tt0111161/"
    assert top["year"] == 1994
    assert top["image"]["link"].startswith("https://")
    types = {r["type"] for r in results}
    assert "movie" in types


# ---- title details ----------------------------------------------------------

def test_details_movie():
    out = parsers.parse_title_details(MOVIE)
    assert out["id"] == "tt0111161"
    assert out["title"] == "The Shawshank Redemption"
    assert out["original_title"] is None          # same as title -> null
    assert out["link"] == "https://www.imdb.com/title/tt0111161/"
    assert out["type"] == "movie"
    assert out["is_series"] is False
    assert out["year"] == 1994
    assert out["release_date"] == "1994-10-14"
    assert out["runtime_minutes"] == 142
    assert out["certificate"] == "R"
    assert out["genres"] == ["Drama"]
    assert out["rating"]["value"] >= 9
    assert out["rating"]["vote_count"] > 2_000_000
    assert out["rating"]["top_rank"] == 1
    assert out["metascore"]["score"] == 82
    assert out["directors"] == [{"id": "nm0001104", "name": "Frank Darabont",
                                 "link": "https://www.imdb.com/name/nm0001104/"}]
    assert len(out["stars"]) == 4
    assert out["top_cast"][0]["name"] == "Tim Robbins"
    assert out["top_cast"][0]["characters"] == ["Andy Dufresne"]
    assert out["total_cast"] > 50
    assert out["box_office"]["budget"]["amount"] == 25_000_000
    assert out["box_office"]["budget"]["currency"] == "USD"
    assert out["box_office"]["gross_worldwide"]["amount"] > 25_000_000
    assert out["seasons"] is None                 # movies have no seasons block
    assert len(out["similar_titles"]) == 12
    assert out["similar_titles"][0]["id"].startswith("tt")
    assert out["countries_of_origin"] == ["United States"]
    assert "English" in out["spoken_languages"]
    # keys the wrapper relies on are always present
    for key in ("plot", "trailer", "image", "metascore", "box_office"):
        assert key in out


def test_details_tv():
    out = parsers.parse_title_details(TV)
    assert out["id"] == "tt0944947"
    assert out["is_series"] is True
    assert out["seasons"] == {"count": 8,
                              "seasons": ["1", "2", "3", "4", "5", "6", "7", "8"],
                              "total_episodes": 74,
                              "is_ongoing": False}
    assert out["creators"] and out["creators"][0]["name"] == "David Benioff"
    assert out["directors"] == []                 # TV shows have creators instead
    assert out["end_year"] == 2019


def test_details_sparse_nulls():
    out = parsers.parse_title_details(SPARSE)
    assert out["id"] == "tt0000001"
    assert out["metascore"] is None
    assert out["box_office"] is None
    assert out["trailer"] is None
    assert out["seasons"] is None
    assert out["rating"]["value"] is not None     # even 1894 shorts are rated


def test_details_missing_stub():
    assert parsers.parse_title_details(MISSING) is None


# ---- cast -------------------------------------------------------------------

def test_cast():
    header, cast, pagination = parsers.parse_cast(_fixture("title_cast_page1.json"))
    assert header == {"id": "tt0944947", "title": "Game of Thrones",
                      "link": "https://www.imdb.com/title/tt0944947/"}
    assert len(cast) == 50
    first = cast[0]
    assert first["name"] == "Peter Dinklage"
    assert first["characters"] == ["Tyrion Lannister"]
    assert first["episodes"]["count"] == 68
    assert first["episodes"]["start_year"] == 2011
    assert pagination["total"] > 800
    assert pagination["has_more"] is True
    assert pagination["next_cursor"]


def test_cast_missing_stub():
    assert parsers.parse_cast(MISSING) is None


# ---- reviews ----------------------------------------------------------------

def test_reviews():
    header, reviews, pagination = parsers.parse_reviews(_fixture("title_reviews_page1.json"))
    assert header["id"] == "tt1375666"
    assert len(reviews) == 25
    first = reviews[0]
    assert first["id"].startswith("rw")
    assert first["title"]
    assert first["text"]
    assert isinstance(first["rating"], int)
    assert first["author"]["id"].startswith("ur")
    assert first["date"].count("-") == 2          # ISO date
    assert isinstance(first["is_spoiler"], bool)
    assert first["helpful_votes"]["up"] is not None
    assert pagination["total"] > 4000
    assert pagination["next_cursor"]


# ---- episodes ---------------------------------------------------------------

def test_seasons():
    out = parsers.parse_seasons(_fixture("title_seasons.json"))
    assert out["id"] == "tt0944947"
    assert out["is_series"] is True
    assert out["seasons"]["count"] == 8
    assert out["seasons"]["total_episodes"] == 74


def test_episodes():
    header, episodes, pagination = parsers.parse_episodes(_fixture("title_episodes_s1.json"))
    assert header["id"] == "tt0944947"
    assert header["is_ongoing"] is False
    aired = [e for e in episodes if e["episode"] and e["episode"] >= 1]
    assert len(aired) == 10                       # GoT S1; specials ride along as ep 0
    ep1 = next(e for e in aired if e["episode"] == 1)
    assert ep1["title"] == "Winter Is Coming"
    assert ep1["season"] == 1
    assert ep1["release_date"] == "2011-04-17"
    assert ep1["rating"]["value"] > 8
    assert pagination["has_more"] is False
    assert pagination["next_cursor"] is None


# ---- person -----------------------------------------------------------------

def test_person():
    out = parsers.parse_person(_fixture("person_details.json"))
    assert out["id"] == "nm0000138"
    assert out["name"] == "Leonardo DiCaprio"
    assert out["link"] == "https://www.imdb.com/name/nm0000138/"
    assert out["bio"]
    assert out["birth"] == {"date": "1974-11-11",
                            "place": "Hollywood, Los Angeles, California, USA"}
    assert out["death"] is None
    assert out["is_dead"] is False
    assert out["height_cm"] == 182.88
    assert "Actor" in out["professions"]
    assert out["star_meter"]["rank"] > 0
    assert len(out["known_for"]) == 8
    assert out["known_for"][0]["role"] == "Actor"
    credits = out["filmography"]["credits"]
    assert credits and credits[0]["id"].startswith("tt")
    assert credits[0]["category"]
    assert out["filmography"]["pagination"]["total"] > 100


def test_person_missing_stub():
    stub = {"name": {"id": "nm9999999999", "nameText": None}}
    assert parsers.parse_person(stub) is None


# ---- search -----------------------------------------------------------------

def test_search():
    results, pagination = parsers.parse_search(_fixture("search_page1.json"))
    assert len(results) == pagination["total"] == 43   # all matrix movies fit one page
    top = results[0]
    assert top["id"] == "tt0133093"
    assert top["title"] == "The Matrix"
    assert top["genres"]
    assert top["rating"]["value"] > 8
    assert pagination["has_more"] is False
    assert pagination["next_cursor"] is None


# ---- charts -----------------------------------------------------------------

def test_chart_titles():
    results, pagination = parsers.parse_chart_titles(_fixture("chart_top_movies_trimmed.json"))
    assert len(results) == 5                      # fixture trimmed to 5 edges
    assert results[0]["rank"] == 1
    assert results[0]["id"] == "tt0111161"
    assert results[0]["title"] == "The Shawshank Redemption"
    assert pagination["total"] == 250


def test_box_office():
    weekend, entries = parsers.parse_box_office(_fixture("chart_box_office.json"))
    assert weekend["start_date"] and weekend["end_date"]
    assert entries
    first = entries[0]
    assert first["rank"] == 1
    assert first["weekend_gross"]["amount"] > 0
    assert first["weekend_gross"]["currency"] == "USD"
    assert first["gross_worldwide"]["amount"] >= first["weekend_gross"]["amount"]


def test_chart_names():
    results, _ = parsers.parse_chart_names(_fixture("chart_popular_celebrities_trimmed.json"))
    assert len(results) == 5                      # fixture trimmed to 5 edges
    first = results[0]
    assert first["rank"] == 1
    assert first["id"].startswith("nm")
    assert first["link"].startswith("https://www.imdb.com/name/")
    assert first["known_for"] is None or first["known_for"]["id"].startswith("tt")

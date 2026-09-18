"""Pure parsers: raw IMDB GraphQL / suggestion payloads -> stable dicts.

Output conventions (repo-wide): snake_case; `link` not `url`; booleans as
is_/has_ questions; identity fields (id, title/name, link) first, then main
content, then ratings/stats, then nested objects, then metadata; ISO dates;
money as numeric amount + separate currency; null (never "" or omitted) for
missing values.

Deliberately dropped raw fields: __typename (noise), displayableProperty /
LocalizedString language wrappers (presentation-only), contribution/reporting
links (imdb-internal), video playbackURLs (expiring signed CDN links — the
stable video page link is emitted instead), suggestion `vq`/`v` video counts.
"""

IMDB = "https://www.imdb.com"


def _dig(obj, *path, default=None):
    for key in path:
        if isinstance(obj, dict):
            obj = obj.get(key)
        elif isinstance(obj, list) and isinstance(key, int) and -len(obj) <= key < len(obj):
            obj = obj[key]
        else:
            return default
        if obj is None:
            return default
    return obj


def _title_link(title_id):
    return f"{IMDB}/title/{title_id}/" if title_id else None


def _person_link(person_id):
    return f"{IMDB}/name/{person_id}/" if person_id else None


def _image(node):
    """Image node -> {link, width, height} (or None)."""
    if not isinstance(node, dict) or not node.get("url"):
        return None
    return {"link": node["url"],
            "width": node.get("width"),
            "height": node.get("height")}


def _money(node):
    """Money node {amount, currency} -> same shape (or None)."""
    amount = _dig(node, "amount")
    if amount is None:
        return None
    return {"amount": amount, "currency": _dig(node, "currency")}


def _iso_date(node):
    """{day, month, year} components -> "YYYY-MM-DD" (partial -> "YYYY-MM"/"YYYY")."""
    if not isinstance(node, dict):
        return None
    year, month, day = node.get("year"), node.get("month"), node.get("day")
    if not year:
        return None
    if not month:
        return f"{year:04d}"
    if not day:
        return f"{year:04d}-{month:02d}"
    return f"{year:04d}-{month:02d}-{day:02d}"


def _minutes(seconds):
    return round(seconds / 60) if seconds else None


def _rating(node):
    """ratingsSummary -> {value, vote_count} (or None when unrated)."""
    if not isinstance(node, dict):
        return None
    if node.get("aggregateRating") is None and not node.get("voteCount"):
        return None
    return {"value": node.get("aggregateRating"),
            "vote_count": node.get("voteCount")}


def _rank_change(node):
    """RankChange/MeterRankChange -> {direction, amount} (or None)."""
    if not isinstance(node, dict):
        return None
    direction = (node.get("changeDirection") or "").lower() or None
    return {"direction": direction, "amount": node.get("difference")}


def _genres(node):
    """titleGenres -> ["Action", ...]."""
    return [g for g in
            (_dig(e, "genre", "text") for e in _dig(node, "genres", default=[]))
            if g]


def _title_card(node):
    """TitleCard fragment payload -> compact title dict (search/charts/similar)."""
    if not isinstance(node, dict):
        return None
    title_id = node.get("id")
    original = _dig(node, "originalTitleText", "text")
    title = _dig(node, "titleText", "text")
    return {
        "id": title_id,
        "title": title,
        "original_title": original if original != title else None,
        "link": _title_link(title_id),
        "type": _dig(node, "titleType", "id"),
        "is_series": _dig(node, "titleType", "canHaveEpisodes", default=False),
        "year": _dig(node, "releaseYear", "year"),
        "end_year": _dig(node, "releaseYear", "endYear"),
        "runtime_minutes": _minutes(_dig(node, "runtime", "seconds")),
        "plot": _dig(node, "plot", "plotText", "plainText"),
        "genres": _genres(node.get("titleGenres")),
        "rating": _rating(node.get("ratingsSummary")),
        "image": _image(node.get("primaryImage")),
    }


def _missing_title(node):
    """True when the payload is a nonexistent-id stub: IMDB's GraphQL echoes
    back {id: ..., titleText: null, ...} instead of a null title."""
    return not isinstance(node, dict) or _dig(node, "titleText", "text") is None


def _missing_person(node):
    """Same stub detection for Name payloads (nameText null)."""
    return not isinstance(node, dict) or _dig(node, "nameText", "text") is None


def _pagination(connection):
    """Connection payload -> {total, next_cursor, has_more}."""
    page = _dig(connection, "pageInfo", default={}) or {}
    has_more = bool(page.get("hasNextPage"))
    return {
        "total": _dig(connection, "total"),
        "next_cursor": page.get("endCursor") if has_more else None,
        "has_more": has_more,
    }


# --- autocomplete ------------------------------------------------------------

def parse_suggestions(payload):
    """v3.sg suggestion payload -> mixed title/person result list."""
    results = []
    for item in payload.get("d") or []:
        item_id = item.get("id") or ""
        image = None
        raw_image = item.get("i")
        if isinstance(raw_image, dict) and raw_image.get("imageUrl"):
            image = {"link": raw_image["imageUrl"],
                     "width": raw_image.get("width"),
                     "height": raw_image.get("height")}
        if item_id.startswith("nm"):
            results.append({
                "id": item_id,
                "type": "person",
                "name": item.get("l"),
                "link": _person_link(item_id),
                "known_for": item.get("s") or None,
                "rank": item.get("rank"),
                "image": image,
            })
        elif item_id.startswith("tt"):
            results.append({
                "id": item_id,
                "type": item.get("qid") or "title",
                "title": item.get("l"),
                "link": _title_link(item_id),
                "year": item.get("y"),
                "year_range": item.get("yr"),
                "stars": item.get("s") or None,
                "rank": item.get("rank"),
                "image": image,
            })
        # anything else (editorial lists etc.) is dropped
    return results


# --- search ------------------------------------------------------------------

def parse_search(data):
    """advancedTitleSearch data -> (results, pagination)."""
    conn = _dig(data, "advancedTitleSearch", default={}) or {}
    results = [_title_card(_dig(e, "node", "title"))
               for e in conn.get("edges") or []]
    return [r for r in results if r], _pagination(conn)


# --- title details -----------------------------------------------------------

def _principal_credits(nodes):
    """principalCredits -> {directors, creators, writers, stars} name lists."""
    out = {"directors": [], "creators": [], "writers": [], "stars": []}
    keymap = {"director": "directors", "creator": "creators",
              "writer": "writers", "cast": "stars"}
    for group in nodes or []:
        key = keymap.get(_dig(group, "category", "id"))
        if not key:
            continue
        for credit in group.get("credits") or []:
            name_id = _dig(credit, "name", "id")
            out[key].append({
                "id": name_id,
                "name": _dig(credit, "name", "nameText", "text"),
                "link": _person_link(name_id),
            })
    return out


def _cast_entry(node):
    name_id = _dig(node, "name", "id")
    entry = {
        "id": name_id,
        "name": _dig(node, "name", "nameText", "text"),
        "link": _person_link(name_id),
        "characters": [c["name"] for c in node.get("characters") or []
                       if isinstance(c, dict) and c.get("name")],
        "image": _image(_dig(node, "name", "primaryImage")),
    }
    return entry


def _seasons_summary(node):
    """Title.episodes -> {count, seasons, total_episodes, is_ongoing} (None for movies)."""
    if not isinstance(node, dict):
        return None
    seasons = [_dig(e, "node", "season")
               for e in _dig(node, "displayableSeasons", "edges", default=[])]
    seasons = [s for s in seasons if s is not None]
    return {
        "count": _dig(node, "displayableSeasons", "total"),
        "seasons": seasons,
        "total_episodes": _dig(node, "episodes", "total"),
        "is_ongoing": node.get("isOngoing"),
    }


def parse_title_details(data):
    """TitleDetails data -> consolidated details dict (None when title missing)."""
    node = data.get("title")
    if _missing_title(node):
        return None
    title_id = node.get("id")
    title = _dig(node, "titleText", "text")
    original = _dig(node, "originalTitleText", "text")
    principals = _principal_credits(node.get("principalCredits"))
    trailer_id = _dig(node, "latestTrailer", "id")

    budget = _money(_dig(node, "productionBudget", "budget"))
    opening = _money(_dig(node, "openingWeekendGross", "gross", "total"))
    if opening:
        opening["weekend_end_date"] = _dig(node, "openingWeekendGross", "weekendEndDate")
        opening["theater_count"] = _dig(node, "openingWeekendGross", "theaterCount")
    gross = _money(_dig(node, "lifetimeGross", "total"))
    box_office = None
    if budget or opening or gross:
        box_office = {"budget": budget, "opening_weekend": opening,
                      "gross_worldwide": gross}

    metascore = None
    if _dig(node, "metacritic", "metascore", "score") is not None:
        metascore = {"score": _dig(node, "metacritic", "metascore", "score"),
                     "review_count": _dig(node, "metacritic", "metascore", "reviewCount")}

    rating = _rating(node.get("ratingsSummary"))
    if rating:
        rating["top_rank"] = _dig(node, "ratingsSummary", "topRanking", "rank")

    trailer = None
    if trailer_id:
        trailer = {
            "id": trailer_id,
            "title": _dig(node, "latestTrailer", "name", "value"),
            "link": f"{IMDB}/video/{trailer_id}/",
            "duration_seconds": _dig(node, "latestTrailer", "runtime", "value"),
            "thumbnail_link": _dig(node, "latestTrailer", "thumbnail", "url"),
        }

    is_series = _dig(node, "titleType", "canHaveEpisodes", default=False)
    return {
        "id": title_id,
        "title": title,
        "original_title": original if original != title else None,
        "link": node.get("canonicalUrl") or _title_link(title_id),
        "type": _dig(node, "titleType", "id"),
        "is_series": is_series,
        "is_episode": _dig(node, "titleType", "isEpisode", default=False),
        "year": _dig(node, "releaseYear", "year"),
        "end_year": _dig(node, "releaseYear", "endYear"),
        "release_date": _iso_date(node.get("releaseDate")),
        "runtime_minutes": _minutes(_dig(node, "runtime", "seconds")),
        "certificate": _dig(node, "certificate", "rating"),
        "plot": _dig(node, "plot", "plotText", "plainText"),
        "genres": _genres(node.get("titleGenres")),
        "rating": rating,
        "metascore": metascore,
        "directors": principals["directors"],
        "creators": principals["creators"],
        "writers": principals["writers"],
        "stars": principals["stars"],
        "top_cast": [_cast_entry(_dig(e, "node", default={}))
                     for e in _dig(node, "credits", "edges", default=[])],
        "total_cast": _dig(node, "credits", "total"),
        "trailer": trailer,
        "image": _image(node.get("primaryImage")),
        "box_office": box_office,
        "seasons": _seasons_summary(node.get("episodes")) if is_series else None,
        "similar_titles": [c for c in
                           (_title_card(_dig(e, "node"))
                            for e in _dig(node, "moreLikeThisTitles", "edges", default=[]))
                           if c],
        "countries_of_origin": [c["text"] for c in
                                _dig(node, "countriesOfOrigin", "countries", default=[])
                                if isinstance(c, dict) and c.get("text")],
        "spoken_languages": [l["text"] for l in
                             _dig(node, "spokenLanguages", "spokenLanguages", default=[])
                             if isinstance(l, dict) and l.get("text")],
    }


# --- title cast --------------------------------------------------------------

def parse_cast(data):
    """TitleCast data -> (title header, cast list, pagination); None when missing."""
    node = data.get("title")
    if _missing_title(node):
        return None
    conn = node.get("credits") or {}
    cast = []
    for edge in conn.get("edges") or []:
        member = edge.get("node") or {}
        entry = _cast_entry(member)
        entry["attributes"] = [a["text"] for a in member.get("attributes") or []
                               if isinstance(a, dict) and a.get("text")]
        episodes = member.get("episodeCredits")
        entry["episodes"] = None
        if isinstance(episodes, dict) and episodes.get("total"):
            entry["episodes"] = {
                "count": episodes.get("total"),
                "start_year": _dig(episodes, "yearRange", "year"),
                "end_year": _dig(episodes, "yearRange", "endYear"),
            }
        cast.append(entry)
    header = {"id": node.get("id"),
              "title": _dig(node, "titleText", "text"),
              "link": _title_link(node.get("id"))}
    return header, cast, _pagination(conn)


# --- title reviews -----------------------------------------------------------

def parse_reviews(data):
    """TitleReviews data -> (title header, review list, pagination); None when missing."""
    node = data.get("title")
    if _missing_title(node):
        return None
    conn = node.get("reviews") or {}
    reviews = []
    for edge in conn.get("edges") or []:
        review = edge.get("node") or {}
        reviews.append({
            "id": review.get("id"),
            "title": _dig(review, "summary", "originalText"),
            "text": _dig(review, "text", "originalText", "plainText"),
            "rating": review.get("authorRating"),
            "author": {"id": _dig(review, "author", "userId"),
                       "nickname": _dig(review, "author", "nickName")},
            "date": review.get("submissionDate"),
            "is_spoiler": review.get("spoiler", False),
            "helpful_votes": {"up": _dig(review, "helpfulness", "upVotes"),
                              "down": _dig(review, "helpfulness", "downVotes")},
        })
    header = {"id": node.get("id"),
              "title": _dig(node, "titleText", "text"),
              "link": _title_link(node.get("id"))}
    return header, reviews, _pagination(conn)


# --- title episodes ----------------------------------------------------------

def parse_seasons(data):
    """TitleSeasons data -> seasons summary dict; None when title missing."""
    node = data.get("title")
    if _missing_title(node):
        return None
    return {
        "id": node.get("id"),
        "title": _dig(node, "titleText", "text"),
        "link": _title_link(node.get("id")),
        "is_series": _dig(node, "titleType", "canHaveEpisodes", default=False),
        "seasons": _seasons_summary(node.get("episodes")),
    }


def _episode_number(value):
    """Episode number text ("7") -> int where possible, else the raw text."""
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return value


def parse_episodes(data):
    """TitleEpisodes data -> (title header, episode list, pagination); None when missing."""
    node = data.get("title")
    if _missing_title(node):
        return None
    conn = _dig(node, "episodes", "episodes", default={}) or {}
    episodes = []
    for edge in conn.get("edges") or []:
        episode = edge.get("node") or {}
        number = _dig(episode, "series", "displayableEpisodeNumber")
        episodes.append({
            "id": episode.get("id"),
            "title": _dig(episode, "titleText", "text"),
            "link": _title_link(episode.get("id")),
            "season": _episode_number(_dig(number, "displayableSeason", "season")),
            "episode": _episode_number(_dig(number, "episodeNumber", "text")),
            "release_date": _iso_date(episode.get("releaseDate")),
            "plot": _dig(episode, "plot", "plotText", "plainText"),
            "rating": _rating(episode.get("ratingsSummary")),
            "image": _image(episode.get("primaryImage")),
        })
    header = {"id": node.get("id"),
              "title": _dig(node, "titleText", "text"),
              "link": _title_link(node.get("id")),
              "is_ongoing": _dig(node, "episodes", "isOngoing")}
    return header, episodes, _pagination(conn)


# --- person details ----------------------------------------------------------

def parse_person(data):
    """PersonDetails data -> consolidated person dict (None when missing)."""
    node = data.get("name")
    if _missing_person(node):
        return None
    person_id = node.get("id")

    birth = None
    birth_date = _iso_date(_dig(node, "birthDate", "dateComponents"))
    birth_place = _dig(node, "birthLocation", "text")
    if birth_date or birth_place:
        birth = {"date": birth_date, "place": birth_place}

    death = None
    death_date = _iso_date(_dig(node, "deathDate", "dateComponents"))
    death_place = _dig(node, "deathLocation", "text")
    if death_date or death_place:
        death = {"date": death_date, "place": death_place}

    height_cm = None
    if _dig(node, "height", "measurement", "unit") == "CENTIMETER":
        height_cm = _dig(node, "height", "measurement", "value")

    star_meter = None
    if _dig(node, "meterRank", "currentRank") is not None:
        star_meter = {"rank": _dig(node, "meterRank", "currentRank"),
                      "change": _rank_change(_dig(node, "meterRank", "rankChange"))}

    known_for = []
    for edge in _dig(node, "knownFor", "edges", default=[]):
        card = _title_card(_dig(edge, "node", "title"))
        if card:
            card["role"] = _dig(edge, "node", "credit", "category", "text")
            known_for.append(card)

    filmography_conn = node.get("credits") or {}
    filmography = []
    for edge in filmography_conn.get("edges") or []:
        credit = edge.get("node") or {}
        title_id = _dig(credit, "title", "id")
        filmography.append({
            "id": title_id,
            "title": _dig(credit, "title", "titleText", "text"),
            "link": _title_link(title_id),
            "type": _dig(credit, "title", "titleType", "id"),
            "year": _dig(credit, "title", "releaseYear", "year"),
            "category": _dig(credit, "category", "text"),
        })

    return {
        "id": person_id,
        "name": _dig(node, "nameText", "text"),
        "link": node.get("canonicalUrl") or _person_link(person_id),
        "image": _image(node.get("primaryImage")),
        "bio": _dig(node, "bio", "text", "plainText"),
        "birth": birth,
        "death": death,
        "is_dead": (node.get("deathStatus") or "ALIVE") != "ALIVE",
        "height_cm": height_cm,
        "professions": [p for p in
                        (_dig(item, "profession", "text")
                         for item in node.get("professions") or [])
                        if p],
        "star_meter": star_meter,
        "known_for": known_for,
        "filmography": {
            "pagination": _pagination(filmography_conn),
            "credits": filmography,
        },
    }


# --- charts ------------------------------------------------------------------

def parse_chart_titles(data):
    """ChartTitles data -> (ranked title list, pagination)."""
    conn = data.get("chartTitles") or {}
    results = []
    for edge in conn.get("edges") or []:
        card = _title_card(edge.get("node"))
        if not card:
            continue
        entry = {"rank": edge.get("currentRank"),
                 "rank_change": _rank_change(edge.get("rankChange"))}
        entry.update(card)
        results.append(entry)
    return results, _pagination(conn)


def parse_box_office(data):
    """BoxOfficeChart data -> (weekend dict, ranked entries)."""
    chart = data.get("boxOfficeWeekendChart") or {}
    weekend = {"start_date": chart.get("weekendStartDate"),
               "end_date": chart.get("weekendEndDate")}
    entries = []
    for rank, entry in enumerate(chart.get("entries") or [], start=1):
        card = _title_card(entry.get("title")) or {}
        row = {"rank": rank}
        row.update(card)
        row["weekend_gross"] = _money(_dig(entry, "weekendGross", "total"))
        row["gross_worldwide"] = _money(_dig(entry, "title", "lifetimeGross", "total"))
        entries.append(row)
    return weekend, entries


def parse_chart_names(data):
    """PopularCelebrities data -> (ranked people list, pagination)."""
    conn = data.get("topMeterNames") or {}
    results = []
    for edge in conn.get("edges") or []:
        node = edge.get("node") or {}
        person_id = node.get("id")
        known_for_title = _dig(node, "knownFor", "edges", 0, "node", "title")
        known_for = None
        if isinstance(known_for_title, dict) and known_for_title.get("id"):
            known_for = {
                "id": known_for_title["id"],
                "title": _dig(known_for_title, "titleText", "text"),
                "link": _title_link(known_for_title["id"]),
                "year": _dig(known_for_title, "releaseYear", "year"),
            }
        results.append({
            "id": person_id,
            "name": _dig(node, "nameText", "text"),
            "link": _person_link(person_id),
            "rank": _dig(node, "meterRank", "currentRank"),
            "rank_change": _rank_change(_dig(node, "meterRank", "rankChange")),
            "professions": [p for p in
                            (_dig(item, "profession", "text")
                             for item in node.get("professions") or [])
                            if p],
            "known_for": known_for,
            "image": _image(node.get("primaryImage")),
        })
    return results, _pagination(conn)

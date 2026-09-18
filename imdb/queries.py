"""GraphQL query texts, enum maps and id normalization for the IMDB scraper.

Every field and enum here was pinned 2026-08-25 against the live schema via
per-type `__type(name:)` introspection (full introspection is blocked
upstream) and then validated with live queries — see the Phase 0 notes:
  - chartTitles chart types: TOP_RATED_MOVIES / TOP_RATED_TV_SHOWS are the
    Top 250 lists; MOST_POPULAR_MOVIES / MOST_POPULAR_TV_SHOWS are the
    MovieMeter/TVMeter charts. Edges carry currentRank + rankChange.
  - topMeterNames is the StarMeter (popular celebrities) chart; rank comes
    from each Name's meterRank field, the edge order matches it.
  - advancedTitleSearch constraints: titleTextConstraint.searchTerm,
    titleTypeConstraint.anyTitleTypeIds (movie / tvSeries / tvMiniSeries),
    genreConstraint.allGenreIds (display-cased ids like "Sci-Fi"),
    releaseDateConstraint.releaseDateRange {start, end} (YYYY-MM-DD).
  - reviews sort: ReviewsSortBy HELPFULNESS_SCORE / SUBMISSION_DATE /
    TOTAL_VOTES / USER_RATING; filter.spoiler: FilterInclusion EXCLUDE.
  - episodes filter: EpisodesFilter.includeSeasons takes season STRINGS
    ("1"); unaired specials ride along as episode "0" entries.
"""
import re

# --- id normalization --------------------------------------------------------

_TITLE_ID_RE = re.compile(r"^tt\d{4,10}$")
_TITLE_URL_RE = re.compile(r"imdb\.com/[^ ]*?/?title/(tt\d{4,10})", re.I)
_PERSON_ID_RE = re.compile(r"^nm\d{4,10}$")
_PERSON_URL_RE = re.compile(r"imdb\.com/[^ ]*?/?name/(nm\d{4,10})", re.I)


def normalize_title_id(value):
    """Accept a bare tt-id or any imdb.com /title/ URL; return the bare id."""
    value = (value or "").strip()
    if _TITLE_ID_RE.match(value):
        return value
    m = _TITLE_URL_RE.search(value)
    if m:
        return m.group(1)
    raise ValueError(
        f"title_id must be an IMDB id like tt0111161 or an imdb.com title URL, got: {value!r}")


def normalize_person_id(value):
    """Accept a bare nm-id or any imdb.com /name/ URL; return the bare id."""
    value = (value or "").strip()
    if _PERSON_ID_RE.match(value):
        return value
    m = _PERSON_URL_RE.search(value)
    if m:
        return m.group(1)
    raise ValueError(
        f"person_id must be an IMDB id like nm0000138 or an imdb.com name URL, got: {value!r}")


_COUNTRY_RE = re.compile(r"^[A-Za-z]{2}$")


def normalize_country(value):
    """Optional 2-letter country -> uppercased (default US); ValueError otherwise."""
    if value in (None, ""):
        return "US"
    value = str(value).strip()
    if not _COUNTRY_RE.match(value):
        raise ValueError(f"country must be a 2-letter code like US or IN, got: {value!r}")
    return value.upper()


# --- enum maps (user-facing value -> GraphQL) --------------------------------

# Our `type` param -> TitleTypeSearchConstraint.anyTitleTypeIds
TITLE_TYPE_IDS = {
    "movie": ["movie", "tvMovie"],
    "tv": ["tvSeries", "tvMiniSeries"],
}

# Our `sort` param -> AdvancedTitleSearchSort. POPULARITY ranks best-first
# ascending (meter rank 1 = most popular); the rest are descending except
# alphabetical.
SEARCH_SORTS = {
    "popularity": {"sortBy": "POPULARITY", "sortOrder": "ASC"},
    "rating": {"sortBy": "USER_RATING", "sortOrder": "DESC"},
    "vote_count": {"sortBy": "USER_RATING_COUNT", "sortOrder": "DESC"},
    "release_date": {"sortBy": "RELEASE_DATE", "sortOrder": "DESC"},
    "alphabetical": {"sortBy": "TITLE_REGIONAL", "sortOrder": "ASC"},
}

# Our `sort` param on reviews -> ReviewsSort.
REVIEW_SORTS = {
    "helpfulness": {"by": "HELPFULNESS_SCORE", "order": "DESC"},
    "newest": {"by": "SUBMISSION_DATE", "order": "DESC"},
    "oldest": {"by": "SUBMISSION_DATE", "order": "ASC"},
    "rating": {"by": "USER_RATING", "order": "DESC"},
    "votes": {"by": "TOTAL_VOTES", "order": "DESC"},
}

# Chart endpoint -> ChartTitleType enum value.
TITLE_CHARTS = {
    "top-movies": "TOP_RATED_MOVIES",
    "top-tv": "TOP_RATED_TV_SHOWS",
    "popular-movies": "MOST_POPULAR_MOVIES",
    "popular-tv": "MOST_POPULAR_TV_SHOWS",
}

# advancedTitleSearch genre ids (GenreSearchConstraint.allGenreIds) —
# validated live: display-cased with hyphens.
GENRES = [
    "Action", "Adventure", "Animation", "Biography", "Comedy", "Crime",
    "Documentary", "Drama", "Family", "Fantasy", "Film-Noir", "Game-Show",
    "History", "Horror", "Music", "Musical", "Mystery", "News", "Reality-TV",
    "Romance", "Sci-Fi", "Short", "Sport", "Talk-Show", "Thriller", "War",
    "Western",
]

# --- shared fragments --------------------------------------------------------

# Compact card used everywhere a list of titles comes back (search, charts,
# similar titles). plot/runtime are on the card because chart/search
# consumers want them without a details call.
TITLE_CARD = """fragment TitleCard on Title {
  id
  titleText { text }
  originalTitleText { text }
  titleType { id text canHaveEpisodes }
  releaseYear { year endYear }
  primaryImage { url width height }
  ratingsSummary { aggregateRating voteCount }
  runtime { seconds }
  plot { plotText { plainText } }
  titleGenres { genres(limit: 3) { genre { text } } }
}"""

# --- queries -----------------------------------------------------------------

TITLE_DETAILS = TITLE_CARD + """
query TitleDetails($id: ID!) {
  title(id: $id) {
    id
    canonicalUrl
    titleText { text }
    originalTitleText { text }
    titleType { id text canHaveEpisodes isSeries isEpisode }
    releaseYear { year endYear }
    releaseDate { day month year }
    runtime { seconds }
    certificate { rating }
    ratingsSummary { aggregateRating voteCount topRanking { rank } }
    metacritic { metascore { score reviewCount } }
    plot { plotText { plainText } }
    titleGenres { genres { genre { text } } }
    primaryImage { url width height caption { plainText } }
    latestTrailer { id name { value } runtime { value unit } thumbnail { url } }
    principalCredits { category { id text } credits(limit: 10) { name { id nameText { text } } } }
    credits(first: 20, filter: { categories: ["cast"] }) {
      total
      edges { node { name { id nameText { text } primaryImage { url } } ... on Cast { characters(limit: 3) { name } } } }
    }
    productionBudget { budget { amount currency } }
    lifetimeGross(boxOfficeArea: WORLDWIDE) { total { amount currency } }
    openingWeekendGross(boxOfficeArea: DOMESTIC) { gross { total { amount currency } } weekendEndDate theaterCount }
    moreLikeThisTitles(first: 12) { edges { node { ...TitleCard } } }
    episodes { isOngoing displayableSeasons(first: 100) { total edges { node { season } } } episodes(first: 1) { total } }
    countriesOfOrigin { countries(limit: 10) { id text } }
    spokenLanguages { spokenLanguages(limit: 10) { id text } }
  }
}"""

TITLE_CAST = """
query TitleCast($id: ID!, $first: Int!, $after: ID) {
  title(id: $id) {
    id
    titleText { text }
    credits(first: $first, after: $after, filter: { categories: ["cast"] }) {
      total
      pageInfo { endCursor hasNextPage }
      edges { node {
        category { id text }
        name { id nameText { text } primaryImage { url width height } }
        ... on Cast { characters(limit: 5) { name } attributes(limit: 3) { text } episodeCredits(first: 1) { total yearRange { year endYear } } }
      } }
    }
  }
}"""

TITLE_REVIEWS = """
query TitleReviews($id: ID!, $first: Int!, $after: ID, $sort: ReviewsSort, $filter: ReviewsFilter) {
  title(id: $id) {
    id
    titleText { text }
    reviews(first: $first, after: $after, sort: $sort, filter: $filter) {
      total
      pageInfo { endCursor hasNextPage }
      edges { node {
        id
        summary { originalText }
        text { originalText { plainText } }
        authorRating
        author { nickName userId }
        submissionDate
        spoiler
        helpfulness { upVotes downVotes }
      } }
    }
  }
}"""

TITLE_SEASONS = """
query TitleSeasons($id: ID!) {
  title(id: $id) {
    id
    titleText { text }
    titleType { id text canHaveEpisodes }
    episodes {
      isOngoing
      displayableSeasons(first: 100) { total edges { node { season text } } }
      episodes(first: 1) { total }
    }
  }
}"""

TITLE_EPISODES = """
query TitleEpisodes($id: ID!, $first: Int!, $after: ID, $filter: EpisodesFilter) {
  title(id: $id) {
    id
    titleText { text }
    episodes {
      isOngoing
      episodes(first: $first, after: $after, filter: $filter) {
        total
        pageInfo { endCursor hasNextPage }
        edges { node {
          id
          titleText { text }
          releaseDate { day month year }
          primaryImage { url }
          ratingsSummary { aggregateRating voteCount }
          plot { plotText { plainText } }
          series { displayableEpisodeNumber { displayableSeason { season } episodeNumber { text } } }
        } }
      }
    }
  }
}"""

PERSON_DETAILS = TITLE_CARD + """
query PersonDetails($id: ID!) {
  name(id: $id) {
    id
    canonicalUrl
    nameText { text }
    primaryImage { url width height }
    bio { text { plainText } }
    birthDate { dateComponents { day month year } }
    birthLocation { text }
    deathDate { dateComponents { day month year } }
    deathLocation { text }
    deathStatus
    height { measurement { value unit } }
    professions(limit: 5) { profession { text } }
    meterRank { currentRank rankChange { changeDirection difference } }
    knownFor(first: 8) { edges { node { title { ...TitleCard } credit { category { text } } } } }
    credits(first: 100, filter: { categories: ["actor", "actress", "director", "writer", "producer"] }) {
      total
      pageInfo { endCursor hasNextPage }
      edges { node { category { id text } title { id titleText { text } titleType { id text } releaseYear { year } } } }
    }
  }
}"""

SEARCH_TITLES = TITLE_CARD + """
query SearchTitles($first: Int!, $after: String, $constraints: AdvancedTitleSearchConstraints!, $sort: AdvancedTitleSearchSort) {
  advancedTitleSearch(first: $first, after: $after, constraints: $constraints, sort: $sort) {
    total
    pageInfo { endCursor hasNextPage }
    edges { node { title { ...TitleCard } } }
  }
}"""

CHART_TITLES = TITLE_CARD + """
query ChartTitles($first: Int!, $after: String, $chartType: ChartTitleType!) {
  chartTitles(first: $first, after: $after, chart: { chartType: $chartType }) {
    total
    pageInfo { endCursor hasNextPage }
    edges { currentRank rankChange { changeDirection difference } node { ...TitleCard } }
  }
}"""

BOX_OFFICE = TITLE_CARD + """
query BoxOfficeChart {
  boxOfficeWeekendChart {
    weekendStartDate
    weekendEndDate
    entries {
      weekendGross { total { amount currency } }
      title { ...TitleCard lifetimeGross(boxOfficeArea: WORLDWIDE) { total { amount currency } } }
    }
  }
}"""

POPULAR_CELEBRITIES = """
query PopularCelebrities($first: Int!, $after: String) {
  topMeterNames(first: $first, after: $after) {
    pageInfo { endCursor hasNextPage }
    edges { node {
      id
      nameText { text }
      primaryImage { url width height }
      professions(limit: 3) { profession { text } }
      meterRank { currentRank rankChange { changeDirection difference } }
      knownFor(first: 1) { edges { node { title { id titleText { text } releaseYear { year } } } } }
    } }
  }
}"""

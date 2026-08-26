<p align="center">
  <img src="https://raw.githubusercontent.com/omkarcloud/botasaurus/master/images/mascot.png" alt="imdb scraper" />
</p>
<div align="center" style="margin-top: 0;">
  <h1>✨ IMDB Scraper 🎬</h1>
  <p><strong>Scrape IMDb movies, TV shows, ratings, cast, reviews, episodes, box office and the Top 250 charts — clean JSON, real-time, no blocks, no proxies.</strong></p>
</div>
<em>
  <h5 align="center">(Programming Language - Python 3)</h5>
</em>
<p align="center">
  <a href="#">
    <img alt="imdb-scraper forks" src="https://img.shields.io/github/forks/omkarcloud/imdb-scraper?style=for-the-badge" />
  </a>
  <a href="#">
    <img alt="Repo stars" src="https://img.shields.io/github/stars/omkarcloud/imdb-scraper?style=for-the-badge&color=yellow" />
  </a>
</p>
<p align="center">
  <img src="https://views.whatilearened.today/views/github/omkarcloud/imdb-scraper.svg" width="80px" height="28px" alt="View" />
</p>

IMDB Scraper turns any IMDb title into clean JSON without the headache of blocks or managing proxies. Feed it a title ID or URL and **one GET request** returns everything: rating with vote count (+ Top 250 rank), Metascore, plot, genres, certificate, directors, stars, top cast with character names, trailer, poster, box office (budget, opening weekend, worldwide gross), similar titles, and the seasons summary for TV shows.

Twelve more endpoints cover search with filters, autocomplete, full cast credits, user reviews, per-season episodes, people (bio + filmography), and the charts everyone builds apps around: **IMDb Top 250 movies and TV shows, MovieMeter, TVMeter, the weekend box office, and StarMeter popular celebrities** — live data across IMDb's 11+ million titles and 14+ million people.

- **Rated Excellent — 4.6 based on 25 reviews** on [Trustpilot](https://www.trustpilot.com/review/omkar.cloud). Our open source work is sponsored by [1000+ devs on GitHub](https://github.com/sponsors/omkarcloud).

[![Try the IMDB Scraper API in the live playground — free, no signup](https://img.shields.io/badge/%E2%96%B6%20Playground-Run%20a%20live%20request%2C%20free-brightgreen?style=for-the-badge)](https://www.omkar.cloud/tools/imdb-scraper/playground?utm_source=github&utm_medium=cpc&utm_content=badge)

[![Free Plan: 200 requests per month](https://img.shields.io/badge/Free%20tier-200%20requests%2Fmonth-blue?style=for-the-badge)](#pricing)

The same scraper is also available on **Apify** and **RapidAPI**:

[![Run on Apify](https://img.shields.io/badge/Run%20on-Apify-blue)](https://apify.com/omkar-cloud/imdb-scraper) [![Run on RapidAPI](https://img.shields.io/badge/Run%20on-RapidAPI-blue?logo=rapidapi)](https://rapidapi.com/Chetan11dev/api/imdb-api/playground)

[![IMDB Scraper API playground — run a live request in your browser, free, no signup](https://raw.githubusercontent.com/omkarcloud/imdb-scraper/master/imdb-scraper-featured-image.png)](https://www.omkar.cloud/tools/imdb-scraper/playground?utm_source=github&utm_medium=cpc&utm_content=hero-image)

## Example: A Full IMDb Title in One Request

One request to the title details API:

```
GET https://imdb-scraper.omkar.cloud/imdb/title/details?title_id=tt4154796
```

```json
{
  "id": "tt4154796",
  "title": "Avengers: Endgame",
  "link": "https://www.imdb.com/title/tt4154796/",
  "type": "movie",
  "year": 2019,
  "release_date": "2019-04-26",
  "runtime_minutes": 181,
  "certificate": "PG-13",
  "plot": "After the devastating events of Avengers: Infinity War (2018), the universe is in ruins. With the help of remaining allies, the Avengers assemble once more in order to reverse Thanos' actions and restore balance to the universe.",
  "genres": ["Action", "Adventure", "Sci-Fi"],
  "rating": { "value": 8.4, "vote_count": 1480430, "top_rank": 74 },
  "metascore": { "score": 78, "review_count": 57 },
  "directors": [
    { "id": "nm0751577", "name": "Anthony Russo", "link": "https://www.imdb.com/name/nm0751577/" },
    { "id": "nm0751648", "name": "Joe Russo", "link": "https://www.imdb.com/name/nm0751648/" }
  ],
  "stars": [
    { "id": "nm0000375", "name": "Robert Downey Jr.", "link": "https://www.imdb.com/name/nm0000375/" },
    { "id": "nm0262635", "name": "Chris Evans", "link": "https://www.imdb.com/name/nm0262635/" }
  ],
  "top_cast": [
    {
      "id": "nm0000375",
      "name": "Robert Downey Jr.",
      "link": "https://www.imdb.com/name/nm0000375/",
      "characters": ["Tony Stark", "Iron Man"],
      "image": { "link": "https://m.media-amazon.com/images/M/MV5BNzg1MTUyNDYxOF5BMl5BanBnXkFtZTgwNTQ4MTE2MjE@._V1_.jpg" }
    }
  ],
  "trailer": {
    "id": "vi2163260441",
    "link": "https://www.imdb.com/video/vi2163260441/",
    "duration_seconds": 66
  },
  "box_office": {
    "budget": { "amount": 356000000, "currency": "USD" },
    "opening_weekend": { "amount": 357115007, "currency": "USD", "weekend_end_date": "2019-04-28", "theater_count": 4662 },
    "gross_worldwide": { "amount": 2799439100, "currency": "USD" }
  },
  "similar_titles": [
    { "id": "tt4154756", "title": "Avengers: Infinity War", "year": 2018, "rating": { "value": 8.4, "vote_count": 1403564 } }
  ],
  "countries_of_origin": ["United States"],
  "spoken_languages": ["English", "Japanese", "Xhosa"]
}
```

*Trimmed for readability — the full response also carries the poster image, writers, total cast count, seasons for TV shows, and 12 similar titles.*

Competitor APIs make you stitch this together from five or six micro-endpoints. Here it's **one call, one request against your quota**.

**[Run this exact request in the Playground — no signup, no key →](https://www.omkar.cloud/tools/imdb-scraper/playground?utm_source=github&utm_medium=cpc&utm_content=example)**

The playground comes prefilled with this request and runs it against the live API in your browser. The JSON it returns is identical to what the API returns.

## Start Getting Data in Minutes

Python and Node.js integration examples are available for every endpoint in the playground, so you can get IMDb data in minutes instead of days.

```python
import requests

# Get everything about a movie in one call
response = requests.get(
    "https://imdb-scraper.omkar.cloud/imdb/title/details",
    params={"title_id": "tt4154796"},
    headers={"API-Key": "YOUR_API_KEY"}
)

print(response.json())
```

## API Reference

All endpoints are GET requests, authenticated with the `API-Key` header. Every endpoint takes an optional `country` (2-letter code, default `US`) that localizes release dates, certificates, and regional titles. Paginated endpoints use cursors: pass back `pagination.next_cursor` as `cursor` for the next page.

### Title Details

▶ [Try it live in the Playground — no key needed →](https://www.omkar.cloud/tools/imdb-scraper/playground?utm_source=github&utm_medium=cpc&utm_content=endpoint-details)

```
GET https://imdb-scraper.omkar.cloud/imdb/title/details?title_id=tt4154796
```

Accepts a title ID (`tt4154796`) or any imdb.com title URL. Returns the full consolidated title object shown in the example above — rating (+ Top 250 rank), Metascore, plot, genres, certificate, release date, runtime, directors/creators/writers/stars, top cast with characters, trailer, poster, box office, seasons summary for TV shows, 12 similar titles, countries, and languages.

---

### Search Titles

▶ [Try it live in the Playground →](https://www.omkar.cloud/tools/imdb-scraper/playground?utm_source=github&utm_medium=cpc&utm_content=endpoint-search)

```
GET https://imdb-scraper.omkar.cloud/imdb/search?query=avengers
```

Search IMDb's 11+ million titles — 50 results per page, each with ID, title, link, type, year, runtime, plot, genres, rating, and poster. At least one of `query`, `type`, `genre`, `start_year`, `end_year` is required, so filters alone work for genre/year browsing (top-rated horror of the 2020s, most popular 90s comedies...).

| Parameter | Description |
|-----------|-------------|
| `query` | Search phrase matched against title names — e.g. `avengers` |
| `type` | `movie` or `tv` |
| `genre` | One of IMDb's 27 genres (`sci_fi`, `horror`, `film-noir`, ... — case-insensitive) |
| `start_year` / `end_year` | Release-year range (1874–2100) |
| `sort` | `popularity` (default), `rating`, `vote_count`, `release_date`, `alphabetical` |
| `cursor` | Pagination cursor from the previous page |

<details>
<summary>Sample Response (click to expand)</summary>

```json
{
  "query": "avengers",
  "sort": "popularity",
  "country": "US",
  "count": 50,
  "results": [
    {
      "id": "tt21357150",
      "title": "Avengers: Doomsday",
      "link": "https://www.imdb.com/title/tt21357150/",
      "type": "movie",
      "is_series": false,
      "year": 2026,
      "runtime_minutes": 165,
      "plot": "Heroes from three different worlds must unite when they're thrust together to confront a catastrophic danger that could destroy everything they know.",
      "genres": ["Action", "Adventure", "Sci-Fi"],
      "rating": null,
      "image": { "link": "https://m.media-amazon.com/images/M/MV5BNGEwYWZkN2UtOTQ5Mi00MGQzLWEzNjYtMWMyNDBkMTkzMWNkXkEyXkFqcGc@._V1_.jpg", "width": 1086, "height": 1610 }
    },
    {
      "id": "tt4154796",
      "title": "Avengers: Endgame",
      "link": "https://www.imdb.com/title/tt4154796/",
      "type": "movie",
      "is_series": false,
      "year": 2019,
      "runtime_minutes": 181,
      "genres": ["Action", "Adventure", "Sci-Fi"],
      "rating": { "value": 8.4, "vote_count": 1480430 },
      "image": { "link": "https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_.jpg", "width": 1382, "height": 2048 }
    }
  ],
  "pagination": { "total": 6075, "next_cursor": "eyJlc1Rva2VuIjpbIjcyMDkwIi...", "has_more": true }
}
```

</details>

---

### Autocomplete

▶ [Try it live in the Playground →](https://www.omkar.cloud/tools/imdb-scraper/playground?utm_source=github&utm_medium=cpc&utm_content=endpoint-autocomplete)

```
GET https://imdb-scraper.omkar.cloud/imdb/autocomplete?query=aveng
```

Typeahead suggestions for a partial query — titles and people mixed, each with ID, link, year / known-for context, and poster. Perfect for search boxes.

<details>
<summary>Sample Response (click to expand)</summary>

```json
{
  "query": "aveng",
  "count": 8,
  "results": [
    {
      "id": "tt21357150",
      "type": "movie",
      "title": "Avengers: Doomsday",
      "link": "https://www.imdb.com/title/tt21357150/",
      "year": 2026,
      "stars": "Robert Downey Jr., Pedro Pascal",
      "rank": 29,
      "image": { "link": "https://m.media-amazon.com/images/M/MV5BNGEwYWZkN2UtOTQ5Mi00MGQzLWEzNjYtMWMyNDBkMTkzMWNkXkEyXkFqcGc@._V1_.jpg", "width": 1086, "height": 1610 }
    },
    {
      "id": "tt4154796",
      "type": "movie",
      "title": "Avengers: Endgame",
      "link": "https://www.imdb.com/title/tt4154796/",
      "year": 2019,
      "stars": "Robert Downey Jr., Chris Evans",
      "rank": 155,
      "image": { "link": "https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_.jpg", "width": 1382, "height": 2048 }
    }
  ]
}
```

</details>

---

### Title Cast

▶ [Try it live in the Playground →](https://www.omkar.cloud/tools/imdb-scraper/playground?utm_source=github&utm_medium=cpc&utm_content=endpoint-cast)

```
GET https://imdb-scraper.omkar.cloud/imdb/title/cast?title_id=tt4154796
```

The complete cast — 50 per page, cursor-paginated — with character names, headshots, credit attributes, and per-actor episode counts with active years for TV shows.

<details>
<summary>Sample Response (click to expand)</summary>

```json
{
  "id": "tt4154796",
  "title": "Avengers: Endgame",
  "link": "https://www.imdb.com/title/tt4154796/",
  "count": 50,
  "results": [
    {
      "id": "nm0000375",
      "name": "Robert Downey Jr.",
      "link": "https://www.imdb.com/name/nm0000375/",
      "characters": ["Tony Stark", "Iron Man"],
      "image": { "link": "https://m.media-amazon.com/images/M/...jpg", "width": 1361, "height": 2048 },
      "attributes": [],
      "episodes": null
    }
  ],
  "pagination": { "total": 169, "next_cursor": "bm0wMDAwNTY5L3R0NDE1NDc5Ni9hY3RyZXNz", "has_more": true }
}
```

</details>

---

### Title Reviews

▶ [Try it live in the Playground →](https://www.omkar.cloud/tools/imdb-scraper/playground?utm_source=github&utm_medium=cpc&utm_content=endpoint-reviews)

```
GET https://imdb-scraper.omkar.cloud/imdb/title/reviews?title_id=tt4154796
```

User reviews — 25 per page, cursor-paginated — with review title, full text, author rating out of 10, helpful votes, and spoiler flags.

| Parameter | Description |
|-----------|-------------|
| `sort` | `helpfulness` (default), `newest`, `oldest`, `rating`, `votes`. Use `newest` for stable deep pagination |
| `include_spoilers` | `false` filters out reviews flagged as spoilers (default `true`) |
| `cursor` | Pagination cursor from the previous page |

<details>
<summary>Sample Response (click to expand)</summary>

```json
{
  "id": "tt4154796",
  "title": "Avengers: Endgame",
  "link": "https://www.imdb.com/title/tt4154796/",
  "sort": "helpfulness",
  "includes_spoilers": true,
  "count": 24,
  "results": [
    {
      "id": "rw11145009",
      "title": "Unforgetable",
      "text": "Of the 22 films in this series, perhaps none will be forever remembered as great films...",
      "rating": 9,
      "author": { "id": "ur212543450", "nickname": "Andy-7189" },
      "date": "2026-01-22",
      "is_spoiler": true,
      "helpful_votes": { "up": 9, "down": 0 }
    }
  ],
  "pagination": { "total": 9737, "next_cursor": "g4xopermtizcsyah7kthvmrurxsmqcby3eodb6xqcwb32vtjnat2kbczmjobstmsy5vfcw6tvdubhnrywwx52", "has_more": true }
}
```

</details>

---

### Title Episodes

▶ [Try it live in the Playground →](https://www.omkar.cloud/tools/imdb-scraper/playground?utm_source=github&utm_medium=cpc&utm_content=endpoint-episodes)

```
GET https://imdb-scraper.omkar.cloud/imdb/title/episodes?title_id=tt2575988&season=1
```

Episodes of one season — 50 per page — with per-episode ratings, air dates, plots, and stills. Omit `season` to get the seasons list (season numbers, total episodes, ongoing flag).

<details>
<summary>Sample Response (click to expand)</summary>

```json
{
  "id": "tt2575988",
  "title": "Silicon Valley",
  "link": "https://www.imdb.com/title/tt2575988/",
  "is_ongoing": false,
  "season": 1,
  "count": 8,
  "results": [
    {
      "id": "tt3222784",
      "title": "Minimum Viable Product",
      "link": "https://www.imdb.com/title/tt3222784/",
      "season": 1,
      "episode": 1,
      "release_date": "2014-04-06",
      "plot": "Richard is a computer programmer. He has to choose between a $10 million deal with Gavin Belson and a $200,000 deal with Peter Gregory...",
      "rating": { "value": 7.7, "vote_count": 3418 },
      "image": { "link": "https://m.media-amazon.com/images/M/MV5BZTJlMzJiMjctNTY3ZS00NzlmLWFkODUtNTU0YThlNmVmM2EzXkEyXkFqcGc@._V1_.jpg" }
    }
  ],
  "pagination": { "total": 8, "next_cursor": null, "has_more": false }
}
```

</details>

---

### Person Details

▶ [Try it live in the Playground →](https://www.omkar.cloud/tools/imdb-scraper/playground?utm_source=github&utm_medium=cpc&utm_content=endpoint-person)

```
GET https://imdb-scraper.omkar.cloud/imdb/person/details?person_id=nm0424060
```

Everything about one person in a single call — bio, birth details, height, professions, StarMeter rank with weekly change, known-for titles with roles, and the full filmography with credit categories. Accepts an `nm` ID or any imdb.com name URL.

<details>
<summary>Sample Response (click to expand)</summary>

```json
{
  "id": "nm0424060",
  "name": "Scarlett Johansson",
  "link": "https://www.imdb.com/name/nm0424060/",
  "image": { "link": "https://m.media-amazon.com/images/M/MV5BMTM3OTUwMDYwNl5BMl5BanBnXkFtZTcwNTUyNzc3Nw@@._V1_.jpg", "width": 1689, "height": 2048 },
  "bio": "Scarlett Ingrid Johansson was born on November 22, 1984 in Manhattan, New York City, New York. Her mother, Melanie Sloan is from a Jewish family...",
  "birth": { "date": "1984-11-22", "place": "Manhattan, New York City, New York, USA" },
  "death": null,
  "is_dead": false,
  "height_cm": 160.02,
  "professions": ["Actress", "Producer", "Director", "Writer", "Soundtrack"],
  "star_meter": { "rank": 95, "change": { "direction": "down", "amount": 11 } },
  "known_for": [
    {
      "id": "tt0335266",
      "title": "Lost in Translation",
      "link": "https://www.imdb.com/title/tt0335266/",
      "year": 2003,
      "rating": { "value": 7.7, "vote_count": 534005 },
      "role": "Actress"
    }
  ],
  "filmography": {
    "credits": [
      { "id": "tt19850008", "title": "The Batman: Part II", "link": "https://www.imdb.com/title/tt19850008/", "type": "movie", "year": 2028, "category": "Actress" }
    ],
    "pagination": { "total": 99, "next_cursor": null, "has_more": false }
  }
}
```

</details>

---

### Charts: Top 250, MovieMeter, Box Office & StarMeter

▶ [Try them live in the Playground →](https://www.omkar.cloud/tools/imdb-scraper/playground?utm_source=github&utm_medium=cpc&utm_content=endpoint-charts)

```
GET https://imdb-scraper.omkar.cloud/imdb/charts/top-movies
GET https://imdb-scraper.omkar.cloud/imdb/charts/top-tv
GET https://imdb-scraper.omkar.cloud/imdb/charts/popular-movies
GET https://imdb-scraper.omkar.cloud/imdb/charts/popular-tv
GET https://imdb-scraper.omkar.cloud/imdb/charts/box-office
GET https://imdb-scraper.omkar.cloud/imdb/charts/popular-celebrities
```

Six chart endpoints, each a single call with no pagination needed:

| Endpoint | Returns |
|----------|---------|
| `/charts/top-movies` | The full IMDb Top 250 movies with rank, rating, votes, plot, poster |
| `/charts/top-tv` | The full IMDb Top 250 TV shows |
| `/charts/popular-movies` | The 100 most popular movies right now (MovieMeter) with weekly rank changes |
| `/charts/popular-tv` | The 100 most popular TV shows right now (TVMeter) |
| `/charts/box-office` | The US weekend box office top 10 with weekend + lifetime grosses |
| `/charts/popular-celebrities` | The 100 most popular people right now (StarMeter) with rank changes |

<details>
<summary>Sample Response — Weekend Box Office (click to expand)</summary>

```json
{
  "chart": "box-office",
  "weekend": { "start_date": "2026-08-21", "end_date": "2026-08-23" },
  "count": 10,
  "results": [
    {
      "rank": 1,
      "id": "tt22084616",
      "title": "Spider-Man: Brand New Day",
      "link": "https://www.imdb.com/title/tt22084616/",
      "year": 2026,
      "rating": { "value": 8, "vote_count": 259696 },
      "weekend_gross": { "amount": 39000155, "currency": "USD" },
      "gross_worldwide": { "amount": 2219901181, "currency": "USD" }
    }
  ]
}
```

</details>

## Pricing

| Plan | Price | Requests/Month |
|------|-------|----------------|
| Free | $0 | 200 |
| Starter | $16 | 20,000 |
| Grow | $48 | 100,000 |
| Scale | $148 | 400,000 |

1 API call = 1 request

Free Plan Available — [create your API key →](https://www.omkar.cloud/auth/sign-up?redirect=/api-key&utm_source=github&utm_medium=cpc&utm_content=pricing-signup). No credit card for the free tier.

## FAQs

### Can I try the API before signing up?

Yes. The playground runs live requests in your browser — free, no account, no API key. [Try it in the Playground →](https://www.omkar.cloud/tools/imdb-scraper/playground?utm_source=github&utm_medium=cpc&utm_content=faq)

### How fresh is the data?

Live. Every response is scraped from IMDb on demand — today's MovieMeter ranks, this weekend's box office, the review posted an hour ago. Frequently-requested responses are served from a short-lived cache so your calls stay fast.

### How do I get IMDb ratings for a movie?

Call `GET /imdb/title/details?title_id=tt4154796` with a title ID or any imdb.com URL. You get the IMDb rating with vote count, the Metascore, and the title's Top 250 rank (when it has one) — plus the plot, cast, box office, and 30+ other fields in the same response.

### How do I get the IMDb Top 250?

`GET /imdb/charts/top-movies` returns all 250 ranked movies in one call — and one request. `/charts/top-tv` does the same for TV shows. MovieMeter, TVMeter, StarMeter, and the weekend box office each have their own single-call endpoint.

### How many reviews and cast members can I get?

All of them. Reviews come 25 per page and the full cast 50 per page, both cursor-paginated with no page cap — follow `pagination.next_cursor` until `has_more` is `false`. Avengers: Endgame has 9,700+ reviews and 169 cast credits, all reachable.

### Can I pass an IMDb URL instead of an ID?

Yes. `title_id` and `person_id` accept a bare ID (`tt4154796`, `nm0424060`) or any imdb.com title/name URL. Use whichever you have.

### What does the `country` parameter do?

It localizes release dates, certificates, and regional title names — pass `country=IN` and Indian release dates and certifications come back. Defaults to `US`.

### Will I get blocked or need proxies?

No. We handle the scraping infrastructure — you call a normal REST API and never touch IMDb directly, so there are no proxies, headless browsers, or CAPTCHAs on your side.

## More Scraper APIs: Google Maps, Trustpilot & More

- **[Google Maps Scraper (3,100+ GitHub Stars)](https://github.com/omkarcloud/google-maps-scraper)** — need tens of thousands of leads? Type a niche and a city ("dentists in New York") and get every matching business as a ready-to-call lead list — name, address, phone, website, emails, rating, and reviews. The free tier alone pulls up to 100K leads a month.

- **[Trustpilot Scraper API](https://github.com/omkarcloud/trustpilot-scraper)** — real-time Trustpilot data for 1.6M+ companies: search companies by keyword, full profiles with rating distributions, every review for any domain. 200 free requests/month.

- **[G2 Scraper API](https://github.com/omkarcloud/g2-scraper)** — G2 product details, reviews, pricing, and ratings for 240,000+ software products, plus each product's website, emails, and social profiles.

- **[Capterra Scraper API](https://github.com/omkarcloud/capterra-scraper)** — the same clean JSON, pointed at Capterra: 5-dimension rating breakdowns, pricing plans, integrations, pros/cons for 108,726 products.

## Support

Built by developers, for developers — when you reach out, you talk to the engineers who built the API, not a support script. Message us anytime and we'll solve your query within 1 working day.


[![Contact Us on WhatsApp about IMDB Scraper](https://raw.githubusercontent.com/omkarcloud/assets/master/images/whatsapp-us.png)](https://api.whatsapp.com/send?phone=918178804274&text=I%20have%20a%20question%20about%20the%20IMDB%20Scraper%20API.)

Email: [happy.to.help@omkar.cloud](mailto:happy.to.help@omkar.cloud?subject=IMDB%20Scraper%20API%20Question)

[![Email Us about IMDB Scraper](https://raw.githubusercontent.com/omkarcloud/assets/master/images/ask-on-email.png)](mailto:happy.to.help@omkar.cloud?subject=IMDB%20Scraper%20API%20Question)

## Love It? Star It! ⭐

From one developer to another: If the IMDB Scraper API saved you time, please [star the repo](https://github.com/omkarcloud/imdb-scraper).

Here's why it matters: most developers judge a scraper by its stars before trying it. Your star helps the next developer — someone deciding whether the IMDb data here is real and reliable — try it with confidence.

It takes only 1 second, and means the world to me.

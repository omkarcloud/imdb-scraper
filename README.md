# IMDb Scraper

IMDb Scraper by Omkar Cloud gives you 🎯 accurate, 🔍 detailed IMDb data as clean JSON — titles, ratings, reviews, cast, episodes, people, and charts.

[**Try it now, no sign-up:**](https://www.omkar.cloud/tools/imdb-scraper/playground) every one of the 13 endpoints runs with one click in the [playground](https://www.omkar.cloud/tools/imdb-scraper/playground). No Sign Up Required.

**Then build on it for free:** 1,000 calls every month, no credit card. Use them to your heart's content ❤️

Also available on:

[![Run on Apify](https://img.shields.io/badge/Apify-blue)](https://apify.com/omkar-cloud/imdb-scraper) [![Run on RapidAPI](https://img.shields.io/badge/RapidAPI-blue?logo=rapidapi)](https://rapidapi.com/Chetan11dev/api/imdb-api/playground)


## Example: A Full IMDb Movie

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

*Trimmed for readability.*

## Get Started

Start in the [playground](https://www.omkar.cloud/tools/imdb-scraper/playground) — try any endpoint with one click, no sign-up required.

Once you're happy with the data, subscribe to the free plan for 1,000 calls per month:

1. [Sign up on Omkar Cloud](https://www.omkar.cloud/auth/sign-up?redirect=/tools/imdb-scraper/playground) — free, no credit card.
2. Open the [IMDb Scraper playground](https://www.omkar.cloud/tools/imdb-scraper/playground) and enter any movie you like.
3. Hit **Get Live Data** to see the JSON.
4. Open the **Code** tab for a ready-to-paste Python or Node.js snippet.

## Endpoints

13 endpoints cover everything you need.

| Endpoint | Path | Returns |
|---|---|---|
| Autocomplete | `/imdb/autocomplete` | Typeahead for titles and people |
| Search Titles | `/imdb/search` | 50 titles per page; filter by type, genre, or year; sortable |
| Title Details | `/imdb/title/details` | Everything about one title in a single call |
| Title Cast | `/imdb/title/cast` | Full credits with character names, 50 per page |
| Title Reviews | `/imdb/title/reviews` | User reviews with full text, 25 per page |
| Title Episodes | `/imdb/title/episodes` | Season list, or one season's episodes with ratings |
| Person Details | `/imdb/person/details` | Bio, StarMeter rank, full filmography |
| Top 250 Movies / TV | `/imdb/charts/top-movies`, `/imdb/charts/top-tv` | All 250 in one call |
| Most Popular Movies / TV | `/imdb/charts/popular-movies`, `/imdb/charts/popular-tv` | MovieMeter / TVMeter top 100 |
| Weekend Box Office | `/imdb/charts/box-office` | US top 10 with weekend and worldwide gross |
| Popular Celebrities | `/imdb/charts/popular-celebrities` | StarMeter top 100 |

## Pricing

Great value, low price.

| Plan | Price | Calls / month | Per 1,000 |
|---|---|---|---|
| **Basic** | **Free** | **1,000** — the most generous free tier | $0 |
| **Pro** | $16/mo | 20,000 | $0.80 |
| **Ultra** | $48/mo | 100,000 | $0.48 |
| **Mega** | $148/mo | 400,000 | $0.37 |

## 💬 Have Questions? We Have Answers.

Have questions or need data we don't expose yet? Just ask.

[![Message Us on WhatsApp about IMDb Scraper](https://raw.githubusercontent.com/omkarcloud/assets/master/images/whatsapp-us.png)](https://api.whatsapp.com/send?phone=918178804274&text=I%20need%20help%20using%20the%20IMDb%20Scraper%20API.)

[![Ask Us by Email about IMDb Scraper](https://raw.githubusercontent.com/omkarcloud/assets/master/images/ask-on-email.png)](mailto:happy.to.help@omkar.cloud?subject=Help%20with%20IMDb%20Scraper%20API&body=I%20need%20help%20using%20the%20IMDb%20Scraper%20API.)

We reply ✅ within one working day. 🩷 Pinky Promise 🤙

## Love It? Star It ⭐

From one developer to another: if IMDb Scraper saved you time, please [star the repo](https://github.com/omkarcloud/imdb-scraper) — it helps other developers find a good IMDb API :)
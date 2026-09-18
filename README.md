# 🎬 IMDb Scraper

IMDb Scraper is a **free and open-source** scraper that gets you **unlimited** detailed IMDb data for free.

## ✨ What Can I Get?

- 🔍 **Search 11M+ titles** — filter by type, genre, year; sort how you like
- 🎬 **Full title details** — cast, Metascore, box office, trailer & more
- 📺 **Episodes, reviews & people** — seasons, full review text, filmographies
- 📈 **All 6 IMDb charts** — Top 250s, Most Popular, Box Office, Celebrities

## 🎥 Example: A Full IMDb Movie

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

## 🚀 Unlimited Free IMDb Data — Get It in 60 Seconds

1️⃣ Clone and install:
```bash
git clone https://github.com/omkarcloud/imdb-scraper
cd imdb-scraper
python -m pip install -r requirements.txt
```

2️⃣ Start the API:
```bash
python run.py
```

3️⃣ Get your first data:
```bash
curl "http://localhost:8000/title/details?title_id=tt4154796"
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
  "genres": ["Action", "Adventure", "Sci-Fi"],
  "rating": { "value": 8.4, "vote_count": 1487872, "top_rank": 74 },
  "metascore": { "score": 78, "review_count": 57 },
  "directors": [
    { "id": "nm0751577", "name": "Anthony Russo", "link": "https://www.imdb.com/name/nm0751577/" },
    { "id": "nm0751648", "name": "Joe Russo", "link": "https://www.imdb.com/name/nm0751648/" }
  ],
  "box_office": {
    "budget": { "amount": 356000000, "currency": "USD" },
    "gross_worldwide": { "amount": 2799439100, "currency": "USD" }
  }
}
```

All 13 endpoints are now live at `http://localhost:8000`.

## 📚 Endpoints

13 endpoints cover everything you need.

| Endpoint | Path | Returns |
|---|---|---|
| Title Details | `/title/details` | Everything about one title in a single call |
| Search Titles | `/search` | 50 titles per page; filter by type, genre, or year; sortable |
| Autocomplete | `/autocomplete` | Typeahead for titles and people |
| Title Cast | `/title/cast` | Full credits with character names, 50 per page |
| Title Reviews | `/title/reviews` | User reviews with full text, 25 per page |
| Title Episodes | `/title/episodes` | Season list, or one season's episodes with ratings |
| Person Details | `/person/details` | Bio, StarMeter rank, full filmography |
| Top 250 Movies / TV | `/charts/top-movies`, `/charts/top-tv` | All 250 in one call |
| Most Popular Movies / TV | `/charts/popular-movies`, `/charts/popular-tv` | MovieMeter / TVMeter top 100 |
| Weekend Box Office | `/charts/box-office` | US top 10 with weekend and worldwide gross |
| Popular Celebrities | `/charts/popular-celebrities` | StarMeter top 100 |


## 🔍 Exploring Parameters

The same API is published on RapidAPI, and its playground is the easiest place to try parameters and see raw responses. Once a request looks right, run it locally for **unlimited free** data.

1. [Subscribe to the free plan](https://rapidapi.com/Chetan11dev/api/imdb255/pricing) — 1,000 calls/month, no credit card.
2. [Try the endpoints in the playground](https://rapidapi.com/Chetan11dev/api/imdb255/playground/apiendpoint_ee818efa-c7bb-4e9e-b5ff-fe9d1e67ffa3) — every param is pre-filled, so you see real data in one click.
3. Copy the generated code and replace `https://imdb255.p.rapidapi.com` with `http://localhost:8000`. It will now run against your local API.

```python
import requests

# generated by the playground, host swapped for the local API
response = requests.get(
    "http://localhost:8000/title/details",
    params={"title_id": "tt4154796"},
)
print(response.json())
```

## 💬 Have Questions? We Have Answers.

You're a developer — we know how hard completing a project can be. So we offer full support: just message us and we'll reply ✅ with a solution within 1 working day.

[![Message Us on WhatsApp about IMDb Scraper](https://raw.githubusercontent.com/omkarcloud/assets/master/images/whatsapp-us.png)](https://api.whatsapp.com/send?phone=918178804274&text=I%20need%20help%20using%20the%20IMDb%20Scraper%20API.)

[![Ask Us by Email about IMDb Scraper](https://raw.githubusercontent.com/omkarcloud/assets/master/images/ask-on-email.png)](mailto:happy.to.help@omkar.cloud?subject=Help%20with%20IMDb%20Scraper%20API&body=I%20need%20help%20using%20the%20IMDb%20Scraper%20API.)

## ⚡ Popular Scrapers by Omkar Cloud

- [**Google Maps Scraper (3,100+ GitHub Stars)**](https://github.com/omkarcloud/google-maps-scraper) — type "dentists in New York", get every business as a ready-to-call lead list: phones, emails, websites & reviews. Up to 100K free leads/month.
- [**G2 Scraper**](https://www.omkar.cloud/tools/g2-scraper) — G2 product details, ratings & AI-found contacts
- [**Website Email Contact Scraper**](https://www.omkar.cloud/tools/website-email-contact-scraper) — emails, phones & socials from any website
- [**AliExpress Scraper**](https://www.omkar.cloud/tools/aliexpress-scraper) — live product details, SKU variants, stock & shipping
- [**Booking Scraper**](https://www.omkar.cloud/tools/booking-scraper) — Booking.com hotels: prices, ratings, rooms & amenities
- [**Etsy Scraper**](https://www.omkar.cloud/tools/etsy-scraper) — Etsy products: prices, discounts, shops & variations

## ⭐ Love It? [Star It ⭐!](https://github.com/omkarcloud/imdb-scraper)

Star the repo ⭐ and become a star hero!

It's just 1 click, but it means the world to me.

[![Star us on GitHub](https://raw.githubusercontent.com/omkarcloud/google-maps-scraper/master/screenshots/star-us.png)](https://github.com/omkarcloud/imdb-scraper)
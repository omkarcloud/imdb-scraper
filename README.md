![IMDb Scraper Featured Image](https://raw.githubusercontent.com/omkarcloud/imdb-scraper/master/imdb-scraper-featured-image.png)

# IMDb Scraper API

Search movies and TV shows, get title details, pull cast & crew, and fetch trending movies from IMDb via a simple REST API. 5,000 free requests/month.

## Key Features

- Search IMDb titles by name with optional type and genre filters
- Get 30+ data points per title (rating, synopsis, cast, financials, posters, trailers)
- Pull complete cast & crew with roles and character names
- Fetch IMDb's Most Popular Movies list in real time
- **5,000 requests/month on free tier**
- Example Response:
```json
{
  "imdb_id": "tt0111161",
  "imdb_url": "https://www.imdb.com/title/tt0111161/",
  "title": "The Shawshank Redemption",
  "original_title": "The Shawshank Redemption",
  "type": "movie",
  "poster": "https://m.media-amazon.com/images/M/MV5BMDAyY2FhYjctNDc5OS00MDNlLThiMGUtY2UxYWVkNGY2ZjljXkEyXkFqcGc@.jpg",
  "content_rating": "R",
  "release_date": "1994-10-14",
  "start_year": 1994,
  "runtime_minutes": 142,
  "genres": ["Drama"],
  "origin_countries": ["US"],
  "rating": 9.3,
  "vote_count": 3159622,
  "metascore": 82,
  "worldwide_gross": 29334033,
  "budget": 25000000
}
```

## Get API Key

Create an account at [omkar.cloud](https://www.omkar.cloud/auth/sign-up?redirect=/api-key) to get your API key.

It takes just 2 minutes to sign up. You get 5,000 free requests every month for detailed IMDb data — more than enough for most developers to get their job done without paying a dime.

This is a well built product, and your search for the best IMDb API ends right here.


## Quick Start

```bash
curl -X GET "https://imdb-scraper-api.omkar.cloud/imdb-scraper/search?query=The%20Shawshank%20Redemption" \
  -H "API-Key: YOUR_API_KEY"
```

```json
{
  "total_results": 1,
  "results": [
    {
      "imdb_id": "tt0111161",
      "imdb_url": "https://www.imdb.com/title/tt0111161/",
      "title": "The Shawshank Redemption",
      "type": "movie",
      "poster": "https://m.media-amazon.com/images/M/MV5BMDAyY2FhYjctNDc5OS00MDNlLThiMGUtY2UxYWVkNGY2ZjljXkEyXkFqcGc@.jpg",
      "content_rating": "R",
      "release_date": "1994-10-14",
      "runtime_minutes": 142,
      "genres": ["Drama"],
      "rating": 9.3,
      "vote_count": 3159622,
      "metascore": 82
    }
  ]
}
```

## Quick Start (Python)

```bash
pip install requests
```

```python
import requests

response = requests.get(
    "https://imdb-scraper-api.omkar.cloud/imdb-scraper/search",
    params={"query": "The Shawshank Redemption"},
    headers={"API-Key": "YOUR_API_KEY"}
)

print(response.json())
```


## API Reference

### Search

```
GET https://imdb-scraper-api.omkar.cloud/imdb-scraper/search
```

#### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `query` | No | — | Partial or full title to search for. Matches substrings. |
| `type` | No | — | Title type: `movie`, `tv_series`, `tv_episode`, `tv_mini_series`, `tv_movie`, `short`, `video_game`. |
| `genre` | No | — | Genre filter: `action`, `adventure`, `animation`, `biography`, `comedy`, `crime`, `documentary`, `drama`, `family`, `fantasy`, `history`, `horror`, `music`, `mystery`, `romance`, `sci_fi`, `sport`, `thriller`, `war`, `western`. |

#### Example

```python
import requests

response = requests.get(
    "https://imdb-scraper-api.omkar.cloud/imdb-scraper/search",
    params={"query": "The Shawshank Redemption"},
    headers={"API-Key": "YOUR_API_KEY"}
)

print(response.json())
```

#### Response

<details>
<summary>Sample Response (click to expand)</summary>

```json
{
  "total_results": 1,
  "results": [
    {
      "imdb_id": "tt0111161",
      "imdb_url": "https://www.imdb.com/title/tt0111161/",
      "title": "The Shawshank Redemption",
      "original_title": "The Shawshank Redemption",
      "type": "movie",
      "poster": "https://m.media-amazon.com/images/M/MV5BMDAyY2FhYjctNDc5OS00MDNlLThiMGUtY2UxYWVkNGY2ZjljXkEyXkFqcGc@.jpg",
      "poster_thumbnails": [
        {
          "url": "https://m.media-amazon.com/images/M/MV5BMDAyY2FhYjctNDc5OS00MDNlLThiMGUtY2UxYWVkNGY2ZjljXkEyXkFqcGc@._V1_QL75_UX280_CR0,0,280,414_.jpg",
          "width": 280,
          "height": 414
        }
      ],
      "trailer_url": "https://www.youtube.com/watch?v=xyXX8LXiNJ4",
      "content_rating": "R",
      "is_adult": false,
      "release_date": "1994-10-14",
      "start_year": 1994,
      "end_year": null,
      "runtime_minutes": 142,
      "genres": ["Drama"],
      "keywords": ["Period Drama", "Prison Drama", "Drama"],
      "origin_countries": ["US"],
      "languages": ["en"],
      "filming_locations": ["Butler, Ohio, USA"],
      "production_companies": [
        {"imdb_id": "co0040620", "name": "Castle Rock Entertainment"}
      ],
      "budget": 25000000,
      "worldwide_gross": 29334033,
      "rating": 9.3,
      "vote_count": 3159622,
      "metascore": 82,
      "external_links": ["https://www.facebook.com/shawshankredemptionfilm/", "https://www.warnerbros.com/movies/shawshank-redemption"]
    }
  ]
}
```

</details>

---

### Title Details

```
GET https://imdb-scraper-api.omkar.cloud/imdb-scraper/title/details
```

#### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `imdb_id` | Yes | — | IMDb title ID (e.g., `tt0111161`). |

#### Example

```python
import requests

response = requests.get(
    "https://imdb-scraper-api.omkar.cloud/imdb-scraper/title/details",
    params={"imdb_id": "tt0111161"},
    headers={"API-Key": "YOUR_API_KEY"}
)

print(response.json())
```

#### Response

Returns everything from Search, plus directors, writers, and full cast & crew with roles and character names.

<details>
<summary>Sample Response (click to expand)</summary>

```json
{
  "imdb_id": "tt0111161",
  "imdb_url": "https://www.imdb.com/title/tt0111161/",
  "title": "The Shawshank Redemption",
  "original_title": "The Shawshank Redemption",
  "type": "movie",
  "poster": "https://m.media-amazon.com/images/M/MV5BMDAyY2FhYjctNDc5OS00MDNlLThiMGUtY2UxYWVkNGY2ZjljXkEyXkFqcGc@.jpg",
  "poster_thumbnails": [
    {
      "url": "https://m.media-amazon.com/images/M/MV5BMDAyY2FhYjctNDc5OS00MDNlLThiMGUtY2UxYWVkNGY2ZjljXkEyXkFqcGc@._V1_QL75_UX280_CR0,0,280,414_.jpg",
      "width": 280,
      "height": 414
    }
  ],
  "trailer_url": "https://www.youtube.com/watch?v=xyXX8LXiNJ4",
  "content_rating": "R",
  "is_adult": false,
  "release_date": "1994-10-14",
  "start_year": 1994,
  "end_year": null,
  "runtime_minutes": 142,
  "genres": ["Drama"],
  "keywords": ["Period Drama", "Prison Drama", "Drama"],
  "origin_countries": ["US"],
  "languages": ["en"],
  "filming_locations": ["Butler, Ohio, USA"],
  "production_companies": [
    {"imdb_id": "co0040620", "name": "Castle Rock Entertainment"}
  ],
  "budget": 25000000,
  "worldwide_gross": 29334033,
  "rating": 9.3,
  "vote_count": 3159622,
  "metascore": 82,
  "external_links": ["https://www.facebook.com/shawshankredemptionfilm/", "https://www.warnerbros.com/movies/shawshank-redemption"],
  "directors": [
    {
      "imdb_id": "nm0001104",
      "imdb_url": "https://www.imdb.com/name/nm0001104/",
      "name": "Frank Darabont",
      "image": null,
      "image_thumbnails": []
    }
  ],
  "writers": [
    {
      "imdb_id": "nm0001104",
      "imdb_url": "https://www.imdb.com/name/nm0001104/",
      "name": "Frank Darabont",
      "image": null,
      "image_thumbnails": []
    },
    {
      "imdb_id": "nm0000175",
      "imdb_url": "https://www.imdb.com/name/nm0000175/",
      "name": "Stephen King",
      "image": null,
      "image_thumbnails": []
    }
  ],
  "cast": [
    {
      "imdb_id": "nm0000209",
      "imdb_url": "https://www.imdb.com/name/nm0000209/",
      "name": "Tim Robbins",
      "image": "https://m.media-amazon.com/images/M/MV5BMTI1OTYxNzAxOF5BMl5BanBnXkFtZTYwNTE5ODI4.jpg",
      "image_thumbnails": [
        {
          "url": "https://m.media-amazon.com/images/M/MV5BMTI1OTYxNzAxOF5BMl5BanBnXkFtZTYwNTE5ODI4._V1_QL75_UX140_CR0,20,140,140_.jpg",
          "width": 140,
          "height": 140
        }
      ],
      "role": "actor",
      "characters": ["Andy Dufresne"]
    },
    {
      "imdb_id": "nm0000151",
      "imdb_url": "https://www.imdb.com/name/nm0000151/",
      "name": "Morgan Freeman",
      "image": "https://m.media-amazon.com/images/M/MV5BMTc0MDMyMzI2OF5BMl5BanBnXkFtZTcwMzM2OTk1MQ@@.jpg",
      "image_thumbnails": [
        {
          "url": "https://m.media-amazon.com/images/M/MV5BMTc0MDMyMzI2OF5BMl5BanBnXkFtZTcwMzM2OTk1MQ@@._V1_QL75_UX140_CR0,20,140,140_.jpg",
          "width": 140,
          "height": 140
        }
      ],
      "role": "actor",
      "characters": ["Ellis Boyd 'Red' Redding"]
    },
    {
      "imdb_id": "nm0348409",
      "imdb_url": "https://www.imdb.com/name/nm0348409/",
      "name": "Bob Gunton",
      "image": "https://m.media-amazon.com/images/M/MV5BOWQ1ZTI1ZDgtMjhmZC00OWExLTliNWQtNzgxNTExZWIwMDJkXkEyXkFqcGc@.jpg",
      "image_thumbnails": [
        {
          "url": "https://m.media-amazon.com/images/M/MV5BOWQ1ZTI1ZDgtMjhmZC00OWExLTliNWQtNzgxNTExZWIwMDJkXkEyXkFqcGc@._V1_QL75_UX140_CR0,20,140,140_.jpg",
          "width": 140,
          "height": 140
        }
      ],
      "role": "actor",
      "characters": ["Warden Norton"]
    }
  ]
}
```

</details>

---

### Title Cast

```
GET https://imdb-scraper-api.omkar.cloud/imdb-scraper/title/cast
```

#### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `imdb_id` | Yes | — | IMDb title ID (e.g., `tt0111161`). |

#### Example

```python
import requests

response = requests.get(
    "https://imdb-scraper-api.omkar.cloud/imdb-scraper/title/cast",
    params={"imdb_id": "tt0111161"},
    headers={"API-Key": "YOUR_API_KEY"}
)

print(response.json())
```

#### Response

Returns the complete cast & crew list — every actor, director, writer, producer, composer, cinematographer, and editor with roles and character names.

<details>
<summary>Sample Response (click to expand)</summary>

```json
[
  {
    "imdb_id": "nm0000209",
    "imdb_url": "https://www.imdb.com/name/nm0000209/",
    "name": "Tim Robbins",
    "image": "https://m.media-amazon.com/images/M/MV5BMTI1OTYxNzAxOF5BMl5BanBnXkFtZTYwNTE5ODI4.jpg",
    "image_thumbnails": [
      {
        "url": "https://m.media-amazon.com/images/M/MV5BMTI1OTYxNzAxOF5BMl5BanBnXkFtZTYwNTE5ODI4._V1_QL75_UX140_CR0,20,140,140_.jpg",
        "width": 140,
        "height": 140
      }
    ],
    "role": "actor",
    "characters": ["Andy Dufresne"]
  },
  {
    "imdb_id": "nm0000151",
    "imdb_url": "https://www.imdb.com/name/nm0000151/",
    "name": "Morgan Freeman",
    "image": "https://m.media-amazon.com/images/M/MV5BMTc0MDMyMzI2OF5BMl5BanBnXkFtZTcwMzM2OTk1MQ@@.jpg",
    "image_thumbnails": [
      {
        "url": "https://m.media-amazon.com/images/M/MV5BMTc0MDMyMzI2OF5BMl5BanBnXkFtZTcwMzM2OTk1MQ@@._V1_QL75_UX140_CR0,20,140,140_.jpg",
        "width": 140,
        "height": 140
      }
    ],
    "role": "actor",
    "characters": ["Ellis Boyd 'Red' Redding"]
  },
  {
    "imdb_id": "nm0348409",
    "imdb_url": "https://www.imdb.com/name/nm0348409/",
    "name": "Bob Gunton",
    "image": "https://m.media-amazon.com/images/M/MV5BOWQ1ZTI1ZDgtMjhmZC00OWExLTliNWQtNzgxNTExZWIwMDJkXkEyXkFqcGc@.jpg",
    "image_thumbnails": [
      {
        "url": "https://m.media-amazon.com/images/M/MV5BOWQ1ZTI1ZDgtMjhmZC00OWExLTliNWQtNzgxNTExZWIwMDJkXkEyXkFqcGc@._V1_QL75_UX140_CR0,20,140,140_.jpg",
        "width": 140,
        "height": 140
      }
    ],
    "role": "actor",
    "characters": ["Warden Norton"]
  },
  {
    "imdb_id": "nm0001104",
    "imdb_url": "https://www.imdb.com/name/nm0001104/",
    "name": "Frank Darabont",
    "image": "https://m.media-amazon.com/images/M/MV5BNjk0MTkxNzQwOF5BMl5BanBnXkFtZTcwODM5OTMwNA@@.jpg",
    "image_thumbnails": [
      {
        "url": "https://m.media-amazon.com/images/M/MV5BNjk0MTkxNzQwOF5BMl5BanBnXkFtZTcwODM5OTMwNA@@._V1_QL75_UX140_CR0,20,140,140_.jpg",
        "width": 140,
        "height": 140
      }
    ],
    "role": "director",
    "characters": []
  },
  {
    "imdb_id": "nm0000175",
    "imdb_url": "https://www.imdb.com/name/nm0000175/",
    "name": "Stephen King",
    "image": "https://m.media-amazon.com/images/M/MV5BMjA2ODIxNDM4Nl5BMl5BanBnXkFtZTYwMjkzMzU1.jpg",
    "image_thumbnails": [
      {
        "url": "https://m.media-amazon.com/images/M/MV5BMjA2ODIxNDM4Nl5BMl5BanBnXkFtZTYwMjkzMzU1._V1_QL75_UX140_CR0,20,140,140_.jpg",
        "width": 140,
        "height": 140
      }
    ],
    "role": "writer",
    "characters": []
  }
]
```

</details>

---

### Most Popular Movies

```
GET https://imdb-scraper-api.omkar.cloud/imdb-scraper/most-popular-movies
```

#### Parameters

No parameters required.

#### Example

```python
import requests

response = requests.get(
    "https://imdb-scraper-api.omkar.cloud/imdb-scraper/most-popular-movies",
    headers={"API-Key": "YOUR_API_KEY"}
)

print(response.json())
```

#### Response

<details>
<summary>Sample Response (click to expand)</summary>

```json
[
  {
    "imdb_id": "tt32897959",
    "imdb_url": "https://www.imdb.com/title/tt32897959/",
    "title": "Wuthering Heights",
    "original_title": "Wuthering Heights",
    "type": "movie",
    "synopsis": "A passionate and tumultuous love story set against the backdrop of the Yorkshire moors, exploring the intense and destructive relationship between Heathcliff and Catherine Earnshaw.",
    "poster": "https://m.media-amazon.com/images/M/MV5BMGFlMTVkMDktZGMzMC00Yjk4LWFmNzEtNTFmMzM2YzM3MWFkXkEyXkFqcGc@.jpg",
    "poster_thumbnails": [
      {
        "url": "https://m.media-amazon.com/images/M/MV5BMGFlMTVkMDktZGMzMC00Yjk4LWFmNzEtNTFmMzM2YzM3MWFkXkEyXkFqcGc@._V1_QL75_UX280_CR0,0,280,414_.jpg",
        "width": 280,
        "height": 414
      }
    ],
    "trailer_url": null,
    "content_rating": "R",
    "is_adult": false,
    "release_date": "2026-02-13",
    "start_year": 2026,
    "end_year": null,
    "runtime_minutes": 136,
    "genres": ["Drama", "Romance"],
    "keywords": ["Costume Drama", "Period Drama", "Psychological Drama", "Steamy Romance", "Drama", "Romance"],
    "origin_countries": ["US", "GB"],
    "languages": ["en"],
    "filming_locations": ["London, England, UK"],
    "production_companies": [
      {"imdb_id": "co0002663", "name": "Warner Bros."},
      {"imdb_id": "co0811855", "name": "MRC Film"},
      {"imdb_id": "co1090055", "name": "Domain Entertainment (II)"}
    ],
    "budget": null,
    "worldwide_gross": 125812668,
    "rating": 6.3,
    "vote_count": 27030,
    "metascore": 55,
    "external_links": ["https://www.wutheringheightsfilm.com/"]
  },
  {
    "imdb_id": "tt27543632",
    "imdb_url": "https://www.imdb.com/title/tt27543632/",
    "title": "The Housemaid",
    "original_title": "The Housemaid",
    "type": "movie",
    "synopsis": "A struggling young woman is relieved by the chance for a fresh start as a maid for a wealthy couple. Soon, she discovers that the family's secrets are far more dangerous than her own.",
    "poster": "https://m.media-amazon.com/images/M/MV5BMGU0ZThmMDUtYmZjMi00MDk5LWE2NTQtYzQ3NWZjNWZkZGE3XkEyXkFqcGc@.jpg",
    "poster_thumbnails": [
      {
        "url": "https://m.media-amazon.com/images/M/MV5BMGU0ZThmMDUtYmZjMi00MDk5LWE2NTQtYzQ3NWZjNWZkZGE3XkEyXkFqcGc@._V1_QL75_UX280_CR0,0,280,414_.jpg",
        "width": 280,
        "height": 414
      }
    ],
    "trailer_url": null,
    "content_rating": "R",
    "is_adult": false,
    "release_date": "2025-12-19",
    "start_year": 2025,
    "end_year": null,
    "runtime_minutes": 131,
    "genres": ["Drama", "Mystery", "Thriller"],
    "keywords": ["Erotic Thriller", "Psychological Drama", "Psychological Thriller", "Suspense Mystery"],
    "origin_countries": ["US"],
    "languages": ["en"],
    "filming_locations": ["Saint Elizabeth University, Morristown, New Jersey, USA"],
    "production_companies": [
      {"imdb_id": "co0006881", "name": "Lionsgate"}
    ],
    "budget": 35000000,
    "worldwide_gross": 354341909,
    "rating": 6.8,
    "vote_count": 83358,
    "metascore": 65,
    "external_links": ["https://thehousemaid.movie/"]
  }
]
```

</details>

## Error Handling

```python
response = requests.get(
    "https://imdb-scraper-api.omkar.cloud/imdb-scraper/search",
    params={"query": "The Shawshank Redemption"},
    headers={"API-Key": "YOUR_API_KEY"}
)

if response.status_code == 200:
    data = response.json()
elif response.status_code == 401:
    # Invalid API key
    pass
elif response.status_code == 429:
    # Rate limit exceeded
    pass
```

## FAQs

### What title types are supported?

Movies, TV series, TV episodes, TV mini-series, TV movies, shorts, and video games.

Pass the `type` parameter to filter search results. For example, `type=tv_series` returns only TV shows.

### Can I search by title or IMDb ID?

Both. Use the Search endpoint with a `query` parameter for title-based lookups. Use Title Details with an `imdb_id` parameter (like `tt0111161`) for direct lookups.

Search supports partial matching — searching "Dark" will return "The Dark Knight", "Dark", "Ozark: The Dark Side", and more.

### What's the difference between Title Details and Title Cast?

**Title Details** returns everything about a title — synopsis, ratings, financials, genres, AND a summary of directors, writers, and top cast members.

**Title Cast** returns the complete cast & crew list for a title — every actor, director, writer, producer, composer, cinematographer, and editor. Use this when you need the full credits.

### Does the Most Popular Movies endpoint need any parameters?

No. Just call it and get the current IMDb trending movies list. No parameters, no configuration. It returns the same list you see on IMDb's "Most Popular Movies" page.

## Rate Limits

| Plan | Price | Requests/Month |
|------|-------|----------------|
| Free | $0 | 5,000 |
| Starter | $25 | 100,000 |
| Grow | $75 | 1,000,000 |
| Scale | $150 | 10,000,000 |

## Questions? We have answers.

Reach out anytime. We will solve your query within 1 working day.

[![Contact Us on WhatsApp about IMDb Scraper](https://raw.githubusercontent.com/omkarcloud/assets/master/images/whatsapp-us.png)](https://api.whatsapp.com/send?phone=918178804274&text=I%20have%20a%20question%20about%20the%20IMDb%20Scraper%20API.)

[![Contact Us on Email about IMDb Scraper](https://raw.githubusercontent.com/omkarcloud/assets/master/images/ask-on-email.png)](mailto:happy.to.help@omkar.cloud?subject=IMDb%20Scraper%20API%20Question)

"""Use the scraper straight from Python — no server needed.

    python main.py

Every function returns the same JSON the API does; results are written to
output/*.json. See README.md → "Use it from Python" for the full function list.
"""
import json
import os

from imdb.charts import get_chart
from imdb.search import search_titles
from imdb.title import get_title_details

os.makedirs("output", exist_ok=True)


def save(name, data):
    path = os.path.join("output", name)
    with open(path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"saved {path}")


if __name__ == "__main__":
    # a tt-id or any imdb.com title link
    save("title_tt4154796.json", get_title_details("tt4154796"))

    # 50 titles per page, filter by type, genre and year
    save("search_sci_fi_2019.json", search_titles(query="avengers", title_type="movie", start_year=2019))

    # all 250 in one call
    save("chart_top_movies.json", get_chart("top-movies"))

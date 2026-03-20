"""
IMDb scraper for Sanjith Punnose (nm15360041)
Fetches film credits and saves to films.json
"""

import requests
import json
import re
import os
from datetime import datetime

IMDB_ID = "nm15360041"
OUTPUT_FILE = "films.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

def fetch_imdb_credits():
    url = f"https://www.imdb.com/name/{IMDB_ID}/"
    print(f"Fetching IMDb page: {url}")

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        html = response.text

        # Extract JSON-LD structured data embedded in IMDb pages
        json_ld_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
        if json_ld_match:
            data = json.loads(json_ld_match.group(1))
            print("Found JSON-LD data")

        # Extract __NEXT_DATA__ which contains full filmography
        next_data_match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html, re.DOTALL)
        if next_data_match:
            next_data = json.loads(next_data_match.group(1))
            print("Found __NEXT_DATA__")
            credits = parse_next_data(next_data)
            if credits:
                return credits

    except Exception as e:
        print(f"Error fetching IMDb: {e}")

    # Fallback: return existing films.json if fetch fails
    if os.path.exists(OUTPUT_FILE):
        print("Using existing films.json as fallback")
        with open(OUTPUT_FILE) as f:
            return json.load(f).get("films", [])

    return []


def parse_next_data(data):
    films = []
    try:
        props = data.get("props", {}).get("pageProps", {})
        
        # Navigate the IMDb data structure for credits
        main_column = props.get("mainColumnData", {})
        credits_section = main_column.get("filmCredits", {}).get("edges", [])

        for edge in credits_section:
            node = edge.get("node", {})
            title_info = node.get("title", {})

            title = title_info.get("titleText", {}).get("text", "")
            year_data = title_info.get("releaseYear", {})
            year = year_data.get("year", "") if year_data else ""
            title_id = title_info.get("id", "")
            category = node.get("category", {}).get("text", "")

            if title:
                films.append({
                    "year": year,
                    "title": title,
                    "role": category,
                    "imdb_id": title_id,
                    "lang": "",
                    "dir": "",
                    "music": ""
                })

        print(f"Parsed {len(films)} films from __NEXT_DATA__")
    except Exception as e:
        print(f"Error parsing next data: {e}")

    return films


def merge_with_existing(new_films, existing_films):
    """Merge new IMDb data with existing enriched data (dir, music, lang)"""
    existing_map = {f["title"].lower(): f for f in existing_films}
    merged = []

    for film in new_films:
        key = film["title"].lower()
        if key in existing_map:
            existing = existing_map[key]
            # Keep enriched fields from existing data
            film["lang"] = existing.get("lang", film.get("lang", ""))
            film["dir"] = existing.get("dir", "")
            film["music"] = existing.get("music", "")
        merged.append(film)

    # Keep any existing films not in new list
    new_titles = {f["title"].lower() for f in new_films}
    for ef in existing_films:
        if ef["title"].lower() not in new_titles:
            merged.append(ef)

    # Sort by year descending
    merged.sort(key=lambda x: int(x["year"]) if str(x["year"]).isdigit() else 0, reverse=True)
    return merged


def main():
    print(f"Starting IMDb sync at {datetime.now().isoformat()}")

    # Load existing data
    existing_films = []
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE) as f:
            existing_films = json.load(f).get("films", [])
        print(f"Loaded {len(existing_films)} existing films")

    # Fetch new data from IMDb
    new_films = fetch_imdb_credits()

    if new_films:
        merged = merge_with_existing(new_films, existing_films)
    else:
        print("No new films fetched, keeping existing data")
        merged = existing_films

    output = {
        "name": "Sanjith Punnose",
        "imdb_id": IMDB_ID,
        "last_updated": datetime.now().isoformat(),
        "total_films": len(merged),
        "films": merged
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(merged)} films to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

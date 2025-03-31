import json
import requests
from scrapy.http import HtmlResponse


def update_ipl_series():
    url = "https://www.cricbuzz.com/cricket-series"
    cricbuzz_resp = requests.get(url)
    response = HtmlResponse(url=url, body=cricbuzz_resp.text, encoding='utf-8')

    series_cards = response.xpath('//a[contains(@href, "/cricket-series/")]/@href').extract()
    updated_series = {}

    for link in series_cards:
        if "indian-premier-league" in link:
            parts = link.split('/')
            series_id = int(parts[2])
            year = parts[3][-4:]
            season_key = f"IPL{year}"
            updated_series[season_key] = series_id

    # Load existing data
    try:
        with open("ipl_series.json", "r") as f:
            existing_series = json.load(f)
    except FileNotFoundError:
        existing_series = {}

    # Merge and save
    existing_series.update(updated_series)

    with open("ipl_series.json", "w") as f:
        json.dump(existing_series, f, indent=2)

    print(f"✅ IPL Series IDs updated: {list(updated_series.keys())}")
    return updated_series


if __name__ == "__main__":
    update_ipl_series()

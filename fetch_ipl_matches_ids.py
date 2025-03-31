import json
import requests
from scrapy.http import HtmlResponse
import time

# IPL Series IDs from Cricbuzz (you can add more years if available)
IPL_SERIES = {
    "IPL2008": 2058,
    "IPL2009": 2059,
    "IPL2010": 2060,
    "IPL2011": 2037,
    "IPL2012": 2115,
    "IPL2013": 2170,
    "IPL2014": 2261,
    "IPL2015": 2330,
    "IPL2016": 2430,
    "IPL2017": 2568,
    "IPL2018": 2676,
    "IPL2019": 2810,
    "IPL2020": 3130,
    "IPL2021": 3472,
    "IPL2022": 4061,
    "IPL2023": 5945,
    "IPL2024": 7607,
    "IPL2025": 9237
}


def fetch_matches_for_season(season, series_id):
    print(f"Fetching {season} data...")
    match_list = []
    url = f"https://www.cricbuzz.com/cricket-series/{series_id}/indian-premier-league-{season[-4:]}/matches"

    try:
        cricbuzz_resp = requests.get(url)
        if cricbuzz_resp.status_code != 200:
            print(f"Failed to fetch {season}. Skipping...")
            return []

        response = HtmlResponse(url=url, body=cricbuzz_resp.text, encoding='utf-8')
        match_cards = response.xpath('//*[@id="series-matches"]/div')

        match_no = 1
        for card in match_cards:
            try:
                match_venue = card.xpath('.//div[3]/div[1]/div/text()').extract_first()
                match_result = card.xpath('.//div[3]/div[1]/a[2]/text()').extract_first() or "NA"
                match_time = card.xpath('.//div[3]/div[2]/div/span[2]/text()').extract_first() or "NA"
                match_name = card.xpath('.//div[3]/div[1]/a/span/text()').extract_first()
                match_href = card.xpath('.//div[3]/div[1]/a/@href').extract_first()

                if match_href and "cricket-scores" in match_href:
                    match_id = match_href.split('cricket-scores/')[1].split('/')[0]
                    match_data = {
                        "match_venue": match_venue.strip() if match_venue else "NA",
                        "match_result": match_result.strip(),
                        "match_time": match_time.strip(),
                        "match_name": match_name.strip() if match_name else "NA",
                        "match_id": match_id,
                        "match_no": match_no,
                        "match_date": "NA"
                    }
                    match_list.append(match_data)
                    match_no += 1
            except Exception as e:
                print(f"Error parsing a match card: {e}")
                continue
        print(f"✅ {season}: {len(match_list)} matches fetched")
    except Exception as e:
        print(f"Error fetching {season}: {e}")

    return match_list


def fetch_all_ipl_matches():
    all_matches = {}
    for season, series_id in IPL_SERIES.items():
        matches = fetch_matches_for_season(season, series_id)
        all_matches[season] = matches
        time.sleep(1)  # Be polite to Cricbuzz server

    with open("match_ids.json", "w") as f:
        json.dump(all_matches, f, indent=2)

    print(f"\n🎯 All IPL seasons saved in match_ids.json")


if __name__ == "__main__":
    fetch_all_ipl_matches()

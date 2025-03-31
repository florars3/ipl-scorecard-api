import json
import requests
from scrapy.http import HtmlResponse
import time

def load_ipl_series():
    with open("ipl_series.json", "r") as f:
        return json.load(f)


def fetch_matches_for_season(season, series_id):
    print(f"🔄 Fetching {season} data...")
    match_list = []
    url = f"https://www.cricbuzz.com/cricket-series/{series_id}/indian-premier-league-{season[-4:]}/matches"

    try:
        cricbuzz_resp = requests.get(url)
        if cricbuzz_resp.status_code != 200:
            print(f"❌ Failed to fetch {season}. Skipping...")
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
                print(f"⚠️ Error parsing match card: {e}")
                continue
        print(f"✅ {season}: {len(match_list)} matches fetched")
    except Exception as e:
        print(f"❗ Error fetching {season}: {e}")

    return match_list


def fetch_all_ipl_matches(season='all', save_to_file=True):
    refreshed_data = {}
    ipl_series = load_ipl_series()

    if season == 'all':
        for season_key, series_id in ipl_series.items():
            matches = fetch_matches_for_season(season_key, series_id)
            refreshed_data[season_key] = matches
            time.sleep(1)  # Respectful scraping
    else:
        year_key = f"IPL{season}"
        if year_key in ipl_series:
            series_id = ipl_series[year_key]
            matches = fetch_matches_for_season(year_key, series_id)
            refreshed_data[year_key] = matches
        else:
            raise ValueError(f"Invalid season: {season}")

    if save_to_file:
        with open("match_ids.json", "w") as f:
            json.dump(refreshed_data, f, indent=2)
        print("📄 match_ids.json updated successfully.")

    return refreshed_data

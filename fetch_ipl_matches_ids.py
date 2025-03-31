import json
import requests
from scrapy.http import HtmlResponse
import time
import os
import logging
import argparse
from flask import Flask, jsonify, request

# ---------- Logging ----------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------- Load IPL Series ----------
def load_ipl_series(file_path="ipl_series.json"):
    if not os.path.exists(file_path):
        logging.error(f"IPL series file '{file_path}' not found.")
        return {}
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error reading {file_path}: {e}")
        return {}


# ---------- Fetch Matches ----------
def fetch_matches_for_season(season, series_id):
    logging.info(f"Fetching {season} data...")
    match_list = []
    url = f"https://www.cricbuzz.com/cricket-series/{series_id}/indian-premier-league-{season[-4:]}/matches"

    try:
        cricbuzz_resp = requests.get(url)
        if cricbuzz_resp.status_code != 200:
            logging.warning(f"Failed to fetch {season}. Skipping...")
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
                logging.error(f"Error parsing a match card: {e}")
                continue
        logging.info(f"✅ {season}: {len(match_list)} matches fetched")
    except Exception as e:
        logging.error(f"Error fetching {season}: {e}")

    return match_list


def fetch_all_ipl_matches(season=None):
    ipl_series = load_ipl_series()
    if not ipl_series:
        logging.error("No IPL series data found. Exiting...")
        return {}

    all_matches = {}

    if season:
        if season not in ipl_series:
            logging.error(f"Season '{season}' not found in IPL series data.")
            return {}
        matches = fetch_matches_for_season(season, ipl_series[season])
        all_matches[season] = matches
    else:
        for season_key, series_id in ipl_series.items():
            matches = fetch_matches_for_season(season_key, series_id)
            all_matches[season_key] = matches
            time.sleep(1)  # Be polite

    with open("match_ids.json", "w") as f:
        json.dump(all_matches, f, indent=2)

    logging.info("🎯 IPL matches saved in match_ids.json")
    return all_matches


# ---------- CLI ----------
def cli():
    parser = argparse.ArgumentParser(description="Fetch IPL match data")
    parser.add_argument("--season", type=str, help="Fetch specific IPL season (e.g., IPL2020)")
    args = parser.parse_args()
    fetch_all_ipl_matches(args.season)


# ---------- Flask API ----------
app = Flask(__name__)

@app.route("/fetch-matches", methods=["GET"])
def fetch_matches_route():
    season = request.args.get("season")
    data = fetch_all_ipl_matches(season)
    return jsonify({"status": "success", "data": data})


if __name__ == "__main__":
    cli()

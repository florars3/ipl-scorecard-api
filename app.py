"""
IPL Live Scorecard API
----------------------
A Flask-based API that scrapes live IPL match data from Cricbuzz and returns structured scorecards.

Features:
---------
1. Get live IPL match scorecard.
2. Get scorecard by IPL match number.
3. Get scorecard by Cricbuzz match ID.
4. List all IPL matches for the current season.
5. (Optional) Refresh match IDs by scraping Cricbuzz (Not implemented yet).

Dependencies:
-------------
- Flask
- Flask-CORS
- Requests
- Scrapy (HtmlResponse)

Folder Structure:
-----------------
- app.py                 # Main Flask API file
- match_ids.json         # Local match mapping file
"""

import json
import flask
import requests
from flask import request
from flask_cors import CORS
from scrapy.http import HtmlResponse

app = flask.Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    """
    Home route to describe API usage.

    Returns:
        str: Instructions for using the API.
    """
    return ("Welcome to the IPL Live Scorecard API!\n\n"
            "Usage:\n"
            "1. /scorecard/live - Get live IPL match scorecard.\n"
            "2. /scorecard?ipl_match_no=match_no - Get IPL scorecard by match number.\n"
            "3. /scorecard/match_id - Get scorecard by Cricbuzz match ID.\n"
            "4. /get_all_matches - List all IPL 2025 matches.\n"
            "5. /get_all_matches_refresh - Refresh match IDs.\n")


@app.route('/scorecard/live', methods=["GET"])
def get_live_match_scorecard():
    """
    Fetch scorecard of the first live IPL match.

    Returns:
        dict: Scorecard of live IPL match or error message.
    """
    live_match_id = fetch_live_ipl_match_id()
    if live_match_id == -1:
        return {"message": "No live IPL match found."}
    return get_entire_scorecard(match_id=live_match_id)


@app.route('/scorecard/<match_id>', methods=["GET"])
@app.route("/scorecard", methods=["GET"])
def get_entire_scorecard(match_id=None):
    """
    Fetch complete IPL match scorecard by match ID or match number.

    Query Parameters:
        ipl_match_no (int): Optional IPL match number.
        match_id (str): Optional Cricbuzz match ID.

    Returns:
        dict: Complete scorecard with batting, bowling, toss, result, and playing XI.
    """
    match_no = request.args.get('ipl_match_no', default=None, type=int)
    if match_no is not None:
        match_id = get_match_id_from_no(match_no)
        if match_id == -1:
            return {"message": "Invalid IPL match number."}
    elif not match_id:
        return {"message": "Provide match_id or ipl_match_no."}

    url = "https://www.cricbuzz.com/api/html/cricket-scorecard/" + str(match_id)
    cricbuzz_resp = requests.get(url)
    response = HtmlResponse(url=url, body=cricbuzz_resp.text, encoding='utf-8')

    playing_eleven = get_playing_eleven(response)
    innings_1_score, innings_2_score = get_scores(response)
    toss = get_toss(response)
    result = get_result_update(response)

    response_json = {
        "Innings1": [{"Batsman": get_batting_scorecard('"innings_1"', response)},
                     {"Bowlers": get_bowling_scorecard('"innings_1"', response)},
                     innings_1_score],
        "Innings2": [{"Batsman": get_batting_scorecard('"innings_2"', response)},
                     {"Bowlers": get_bowling_scorecard('"innings_2"', response)},
                     innings_2_score],
        "Result": result,
        "Playing_Eleven": playing_eleven,
        "Toss_Result": toss
    }

    return response_json


@app.route('/get_all_matches', methods=["GET"])
def get_all_matches():
    """
    Returns the list of all IPL matches stored locally in match_ids.json.

    Returns:
        dict: Match number to Match ID mapping.
    """
    with open("./match_ids.json", "r") as f:
        match_ids = json.load(f)
    return match_ids


def fetch_live_ipl_match_id():
    """
    Scrape Cricbuzz Live Scores page to find the first live IPL match ID.

    Returns:
        str: Cricbuzz match ID if found, else -1.
    """
    url = "https://www.cricbuzz.com/cricket-match/live-scores"
    try:
        cricbuzz_resp = requests.get(url)
        response = HtmlResponse(url=url, body=cricbuzz_resp.text, encoding='utf-8')
        live_links = response.xpath('//a[contains(@href, "/live-cricket-scores/")]/@href').extract()
        for link in live_links:
            if "premier-league" in link.lower() or "ipl" in link.lower():
                match_id = link.split('/')[2]
                return match_id
        return -1
    except Exception as e:
        print(f"Error fetching live match ID: {e}")
        return -1


def get_match_id_from_no(match_no):
    """
    Retrieve Cricbuzz match ID based on IPL match number.

    Args:
        match_no (int): IPL match number.

    Returns:
        str: Cricbuzz match ID if found, else -1.
    """
    with open("./match_ids.json", "r") as f:
        match_ids = json.load(f)
    for match in match_ids["IPL2025"]:
        if match['match_no'] == match_no:
            return match['match_id']
    return -1


# --------------- Scraper Utility Functions ---------------

def get_scores(response):
    """
    Extract innings scores from Cricbuzz scorecard HTML.

    Args:
        response (HtmlResponse): Scrapy HTML response.

    Returns:
        tuple: Innings 1 and Innings 2 score dictionaries.
    """
    try:
        innings_1_score = {}
        team1 = response.xpath('//*[@id="innings_1"]/div[1]/div[1]/span[1]/text()').extract()[0].replace("Innings", "").strip()
        score1 = response.xpath('//*[@id="innings_1"]/div[1]/div[1]/span[2]/text()').extract()[0].replace("Innings", "").strip()
        innings_1_score = {
            "team": team1,
            "score": score1,
            "runs": int(score1.split('-')[0].strip()),
            "wickets": int(score1.split('-')[1].split('(')[0].strip()),
            "overs": score1.split('(')[1].split(')')[0].replace('Ov', '').strip()
        }
    except:
        innings_1_score = {}

    try:
        innings_2_score = {}
        team2 = response.xpath('//*[@id="innings_2"]/div[1]/div[1]/span[1]/text()').extract()[0].strip().replace("Innings", "").strip()
        score2 = response.xpath('//*[@id="innings_2"]/div[1]/div[1]/span[2]/text()').extract()[0].strip().replace("Innings", "").strip()
        innings_2_score = {
            "team": team2,
            "score": score2,
            "runs": int(score2.split('-')[0].strip()),
            "wickets": int(score2.split('-')[1].split('(')[0].strip()),
            "overs": score2.split('(')[1].split(')')[0].replace('Ov', '').strip()
        }
    except:
        innings_2_score = {}

    return innings_1_score, innings_2_score


def get_playing_eleven(response):
    """
    Extract playing XI from scorecard.

    Args:
        response (HtmlResponse): Scrapy HTML response.

    Returns:
        dict: Team-wise playing eleven.
    """
    try:
        playing_eleven = {}
        team_name_one = response.xpath(f'/html/body/div[4]/div[2]/div[9]/text()').extract()[0].replace('Squad', '').strip()
        team_one_playing_eleven = response.xpath(f'/html/body/div[4]/div[2]/div[10]/div[2]/a/text()').extract()
        team_name_two = response.xpath(f'/html/body/div[4]/div[2]/div[12]/text()').extract()[0].replace('Squad', '').strip()
        team_two_playing_eleven = response.xpath(f'/html/body/div[4]/div[2]/div[13]/div[2]/a/text()').extract()
        playing_eleven = {team_name_one: team_one_playing_eleven, team_name_two: team_two_playing_eleven}
    except Exception:
        playing_eleven = {}
    return playing_eleven


def get_toss(response):
    """
    Extract toss result from scorecard.

    Args:
        response (HtmlResponse): Scrapy HTML response.

    Returns:
        dict: Toss details.
    """
    try:
        toss = {}
        toss_text = response.xpath('/html/body/div[4]/div[2]/div[3]/div[2]/text()').extract()[0].strip()
        toss_won_by = toss_text.split('won')[0].strip()
        chosen_to = toss_text.split('opt to')[1].strip()
        toss["update"] = toss_text
        toss["winning_team"] = toss_won_by
        toss["chose_to"] = chosen_to
    except:
        toss = {}
    return toss


def get_result_update(response):
    """
    Extract match result from scorecard.

    Args:
        response (HtmlResponse): Scrapy HTML response.

    Returns:
        dict: Match result.
    """
    try:
        result = response.xpath('/html/body/div[1]/text()').extract()[0].strip().lower()
        if "won" not in result:
            final_result = "Not Completed"
            margin = "NA"
        else:
            final_result = result.split('won')[0].replace('(', '').replace("match tied", "").strip()
            margin = result.split('by')[1].strip()
    except:
        final_result, margin, result = "NA", "NA", "NA"
    return {"winning_team": final_result, "update": result, "winning_margin": margin}


def get_batting_scorecard(innings, response):
    """
    Extract batting scorecard.

    Args:
        innings (str): Innings identifier.
        response (HtmlResponse): Scrapy HTML response.

    Returns:
        list: List of batsman stats.
    """
    batting = []
    for i in range(3, 13):
        try:
            batsman_name = response.xpath(f'//*[@id={innings}]/div[1]/div[{i}]/div[1]/a/text()').extract()[0].strip()
            batsman = {
                "name": batsman_name,
                "dismissal": response.xpath(f'//*[@id={innings}]/div[1]/div[{i}]/div[2]/span/text()').extract()[0].strip(),
                "runs": response.xpath(f'//*[@id={innings}]/div[1]/div[{i}]/div[3]/text()').extract()[0].strip(),
                "balls": response.xpath(f'//*[@id={innings}]/div[1]/div[{i}]/div[4]/text()').extract()[0].strip(),
                "fours": response.xpath(f'//*[@id={innings}]/div[1]/div[{i}]/div[5]/text()').extract()[0].strip(),
                "sixes": response.xpath(f'//*[@id={innings}]/div[1]/div[{i}]/div[6]/text()').extract()[0].strip(),
                "sr": response.xpath(f'//*[@id={innings}]/div[1]/div[{i}]/div[7]/text()').extract()[0].strip()
            }
            batting.append(batsman)
        except:
            pass
    return batting


def get_bowling_scorecard(innings, response):
    """
    Extract bowling scorecard.

    Args:
        innings (str): Innings identifier.
        response (HtmlResponse): Scrapy HTML response.

    Returns:
        list: List of bowler stats.
    """
    bowling = []
    for i in range(2, 13):
        try:
            bowler_name = response.xpath(f'//*[@id={innings}]/div[4]/div[{i}]/div[1]/a/text()').extract()[0].strip()
            bowler = {
                "name": bowler_name,
                "overs": response.xpath(f'//*[@id={innings}]/div[4]/div[{i}]/div[2]/text()').extract()[0].strip(),
                "maidens": response.xpath(f'//*[@id={innings}]/div[4]/div[{i}]/div[3]/text()').extract()[0].strip(),
                "runs": response.xpath(f'//*[@id={innings}]/div[4]/div[{i}]/div[4]/text()').extract()[0].strip(),
                "wicket": response.xpath(f'//*[@id={innings}]/div[4]/div[{i}]/div[5]/text()').extract()[0].strip(),
                "economy": response.xpath(f'//*[@id={innings}]/div[4]/div[{i}]/div[8]/text()').extract()[0].strip()
            }
            bowling.append(bowler)
        except:
            pass
    return bowling


if __name__ == "__main__":
    print("* Starting Live Scorecard API...")
    app.run(debug=True, port=5000)

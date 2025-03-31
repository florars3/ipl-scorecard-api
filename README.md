🏏 IPL Live Scorecard API
A Flask-based API that scrapes live IPL match scorecards from Cricbuzz and provides structured, JSON-formatted match data including scores, playing XI, toss results, and match outcomes.

---

🚀 Features
Get the Live IPL Match scorecard.

Get IPL scorecard by Cricbuzz Match ID.

Get IPL scorecard by Match Number.

List all IPL 2025 matches.

(Optional) Refresh match IDs dynamically.

---

📂 Project Structure

Each file has the following purpose:

├──  **app.py**: Contains the main source code for the Flask API.

├──  **match_ids.json**: Stores the mapping of match numbers to match IDs.

├──  **requirements.txt**: Lists the Python dependencies required for the project.

├──  **Dockerfile**: Provides an optional setup for running the project in a Docker container.

├──  **.gitignore**: Specifies files and directories to be ignored by Git.

└──  **README.md**: Documents details about the project.

---

🛠️ Requirements

Python 3.8+

Pip packages:

```
pip install -r requirements.txt
```
Or manually:
```
pip install flask flask-cors requests scrapy
```
---

▶️ Running the API

Locally

1. Clone the repository:
```git clone https://github.com/your-username/ipl-live-scorecard-api.git
cd ipl-live-scorecard-api
```

2. Install dependencies:

```
pip install -r requirements.txt
```
3. Run the server:
```
python app.py
```

The API will be available at:
```
http://localhost:5000/
```

---

Using Docker (Optional)

Build Docker Image
```
docker build -t ipl-live-api .
```

Run Docker Container
```
docker run -d -p 5000:5000 ipl-live-api
```

---

📄 API Endpoints

Home

GET /

Returns usage guide and available endpoints.

---

Get Live Match Scorecard

GET /scorecard/live

Fetches scorecard of the first live IPL match.

Example
```
http://localhost:5000/scorecard/live
```

---

Get Scorecard by Match ID

GET /scorecard/{match_id}

Fetch complete scorecard by Cricbuzz match ID.

Example
```
http://localhost:5000/scorecard/115032
```

Get Scorecard by Match Number

GET /scorecard?ipl_match_no={match_no}

Fetch scorecard by IPL match number (mapped in match_ids.json).

Example
```
http://localhost:5000/scorecard?ipl_match_no=12
```

---

Get All Match IDs

GET /get_all_matches

Returns the locally stored IPL match numbers and IDs from match_ids.json.

---

📝 Example Response

```
{
  "Innings1": [
    {
      "Batsman": [
        {
          "balls": "16",
          "dismissal": "c Naman Dhir b Hardik Pandya",
          "fours": "3",
          "name": "Angkrish Raghuvanshi",
          "runs": "26",
          "sixes": "1",
          "sr": "162.50"
        },
        {
          "balls": "9",
          "dismissal": "c Rickelton b D Chahar",
          "fours": "0",
          "name": "Venkatesh Iyer",
          "runs": "3",
          "sixes": "0",
          "sr": "33.33"
        },
        {
          "balls": "14",
          "dismissal": "c Naman Dhir b Ashwani Kumar",
          "fours": "1",
          "name": "Rinku Singh",
          "runs": "17",
          "sixes": "1",
          "sr": "121.43"
        },
        {
          "balls": "14",
          "dismissal": "b Ashwani Kumar",
          "fours": "2",
          "name": "Manish Pandey",
          "runs": "19",
          "sixes": "1",
          "sr": "135.71"
        },
        {
          "balls": "11",
          "dismissal": "b Ashwani Kumar",
          "fours": "1",
          "name": "Andre Russell",
          "runs": "5",
          "sixes": "0",
          "sr": "45.45"
        },
        {
          "balls": "11",
          "dismissal": "batting",
          "fours": "1",
          "name": "Ramandeep Singh",
          "runs": "22",
          "sixes": "2",
          "sr": "200.00"
        },
        {
          "balls": "8",
          "dismissal": "c Naman Dhir b Vignesh Puthur",
          "fours": "0",
          "name": "Harshit Rana",
          "runs": "4",
          "sixes": "0",
          "sr": "50.00"
        }
      ]
    },
    {
      "Bowlers": [
        {
          "economy": "8.00",
          "maidens": "0",
          "name": "Ashwani Kumar",
          "overs": "3",
          "runs": "24",
          "wicket": "4"
        },
        {
          "economy": "5.00",
          "maidens": "0",
          "name": "Hardik Pandya (c)",
          "overs": "2",
          "runs": "10",
          "wicket": "1"
        },
        {
          "economy": "10.50",
          "maidens": "0",
          "name": "Vignesh Puthur",
          "overs": "2",
          "runs": "21",
          "wicket": "1"
        }
      ]
    },
    {
      "overs": "16.1",
      "runs": 116,
      "score": "116-9 (16.1 Ov)",
      "team": "Kolkata Knight Riders",
      "wickets": 9
    }
  ],
  "Innings2": [
    {
      "Batsman": []
    },
    {
      "Bowlers": []
    },
    {}
  ],
  "Playing_Eleven": {},
  "Result": {
    "update": "mumbai indians opt to bowl",
    "winning_margin": "NA",
    "winning_team": "Not Completed"
  },
  "Toss_Result": {}
}

```

---

🚧 To-Do (Optional)

Add /get_all_matches_refresh to auto-fetch latest match IDs.

Add pagination and match filtering.

Docker Compose setup.

Add unit tests and CI/CD pipeline.

---

⚠️ Disclaimer

This API scrapes data from Cricbuzz for personal use and learning purposes only.
It is not affiliated with Cricbuzz or any official cricket board.
Use responsibly and do not overload Cricbuzz servers.

---


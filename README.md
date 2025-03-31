
# 🏏 IPL Live Scorecard API

A Flask-based API that scrapes **live IPL match scorecards** from Cricbuzz and provides structured, JSON-formatted match data including scores, playing XI, toss results, and match outcomes.

---

## 🚀 Features

- Get **live IPL match scorecard** (auto-detect ongoing match).
- Get IPL scorecard by **Cricbuzz Match ID**.
- Get IPL scorecard by **Match Number**.
- List **all IPL matches** with match IDs.
- **Refresh and populate match IDs dynamically** for all seasons (2008–2025) using `/get_all_matches_refresh`.
- **Update IPL series IDs dynamically** for new seasons using `/update_series`

---

## 📂 Project Structure

```
.
.
├── app.py                  # Flask API source code
├── match_ids.json          # Stores IPL match IDs and details
├── ipl_series.json         # Stores IPL series IDs mapping (season -> series_id)
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker setup (optional)
├── .gitignore              # Git ignored files
├── README.md               # Project documentation
└── utils/                  # Utility scripts
    ├── fetcher.py          # Fetch match IDs logic
    └── update_series.py    # Script to scrape and update IPL series IDs
```

---

## 🛠️ Requirements

- Python 3.8+
- Pip packages:
  ```
  pip install -r requirements.txt
  ```
  Or manually:
  ```
  pip install flask flask-cors requests scrapy
  ```

---

## ▶️ Running the API

### Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/ipl-live-scorecard-api.git
   cd ipl-live-scorecard-api
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server:**
   ```bash
   python app.py
   ```

The API will be available at:
```
http://localhost:5000/
```

---

### Using Docker (Optional)

1. **Build Docker Image:**
   ```bash
   docker build -t ipl-live-api .
   ```

2. **Run Docker Container:**
   ```bash
   docker run -d -p 5000:5000 ipl-live-api
   ```

---

## 📄 API Endpoints

### Home

```
GET /
```
Returns usage guide and available endpoints.

---

### Get Live Match Scorecard

```
GET /scorecard/live
```
Fetches scorecard of the **first live IPL match** (auto-detected).

Example:
```
http://localhost:5000/scorecard/live
```

---

### Get Scorecard by Match ID

```
GET /scorecard/{match_id}
```
Fetch scorecard by **Cricbuzz match ID**.

Example:
```
http://localhost:5000/scorecard/115032
```

---

### Get Scorecard by Match Number

```
GET /scorecard?ipl_match_no={match_no}
```
Fetch scorecard by **IPL match number** (mapped in match_ids.json).

Example:
```
http://localhost:5000/scorecard?ipl_match_no=12
```

---

### Get All Match IDs

```
GET /get_all_matches
```
Returns the stored IPL match numbers and IDs from `match_ids.json`.

---

### Refresh Match IDs (Optional)

```
GET /get_all_matches_refresh
```
Refresh and populate match IDs dynamically for ***all seasons (2008–2025)***.

---

### Refresh a specific season (Optional):

```bash
GET /get_all_matches_refresh?season=2025
```

---

### Update IPL Series IDs (Optional)

```bash
GET /update_series
```
Fetches and updates the latest ***IPL series IDs*** dynamically in `ipl_series.json`.

---

## 🚧 To-Do (Optional)

- Add `/get_all_matches_refresh` to auto-fetch and update match IDs.
- Add pagination and match filtering.
- Add unit tests and CI/CD pipeline.
- Add Docker Compose support.

---

## ⚠️ Disclaimer

This API scrapes data from Cricbuzz **for personal use and learning purposes only.**  
It is **not affiliated** with Cricbuzz or any official cricket board.  
Use responsibly and avoid overloading Cricbuzz servers.


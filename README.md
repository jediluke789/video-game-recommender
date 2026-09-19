# Video Game Search & Favorites Tracker

A full-stack web application built with Python (Flask), JavaScript (jQuery/AJAX), SQLite, and HTML and CSS. The application allows users to search through 500,000+ titles using the RAWG Video Games Database API, view detailed game metadata, and manage an isolated, personalized favorites collection in real time.

---

* **Live Demo:** https://video-game-recommender-9sdk.onrender.com/

---

# Features:
- **Real-Time Game Search:** Queries the RAWG REST API for accurate titles, cover art, release dates, and Metacritic/community ratings.
- **Asynchronous Interactions (AJAX):** Allows adding favorites instantly without triggering full-page reloads.
- **Session-Isolated User Storage:** Uses  UUIDs and cookies to ensure each user's favorites list remains private without requiring a formal sign-in flow.
- **Duplicate Prevention:** Leverages SQLite compound unique constraints `UNIQUE(user_id, name)` and frontend state checks to disable buttons on already-favorited games.
- **Production Ready:** Configured to run behind the Waitress production WSGI server and deployed on Render.

---

## Tech Stack Used: 
- **Frontend**: HTML5, CSS, Javascript, jQuery, AJAX
- **Backend**: Python, Flask, Jinja, Waitress
- **Databases**: SQLite3
- **External API:**: RAWG Video Games Database API --> (https://rawg.io/apidocs)
- **Deployment**: Render, python-dotenv, Git/Github

## Local Setupt and Installation

### Pre reqs
- Python 3.147 (3.10+ should work fine)
- Free personal RAWG API Key (https://rawg.io/apidocs)

### 1. Clone the repository
```bash
git clone https://github.com/jediluke789/video-game-searcher.git
cd your-repo-name
```
### 2. Create and activate the virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate
# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Configure Environment variables
```bash
cp .env.example .env
```
### 5. Add credentials
```bash
API_KEY=your_rawg_api_key_here
FLASK_SECRET_KEY=your_random_secret_key_here
```
### 6. Run application
```bash
python server.py
```
- Then navigate to http://localhost:8000
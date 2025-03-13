import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Title
st.title("🏀 College Basketball Betting Dashboard")

# Function to scrape ESPN NCAA data for today's games
def get_espn_ncaa_data():
    today = datetime.today().strftime('%Y%m%d')
    url = f"https://www.espn.com/mens-college-basketball/scoreboard/_/date/{today}"
    headers = {"User-Agent": "Mozilla/5.0"}  # Mimic a real browser request
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    games = []
    for game in soup.find_all("article", class_="scoreboard" ):
        teams = game.find_all("span", class_="sb-team-short")
        odds = game.find_all("div", class_="odds-details")
        
        if len(teams) == 2:
            team1 = teams[0].text.strip()
            team2 = teams[1].text.strip()
            
            # Extract odds if available
            odds_text = odds[0].text.strip() if odds else "N/A"
            
            games.append({"Home Team": team1, "Away Team": team2, "Odds": odds_text})
    
    return pd.DataFrame(games)

# Fetch live NCAA data from ESPN
ncaa_data = get_espn_ncaa_data()

# Display all games
st.write("### All Men's College Basketball Games Today")
st.table(ncaa_data)

st.write("🔹 This dashboard now pulls today's NCAA games and live odds from ESPN!")

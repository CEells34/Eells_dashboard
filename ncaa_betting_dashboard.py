import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# Title
st.title("🏀 College Basketball Betting Dashboard")

# Function to fetch data from The Odds API
def get_sports_odds():
    API_KEY = "your_api_key_here"  # Replace with your actual API key
    url = "https://api.the-odds-api.com/v4/sports/basketball_ncaab/odds"
    params = {
        "apiKey": API_KEY,
        "regions": "us",
        "markets": "h2h,spreads,totals",
        "oddsFormat": "decimal"
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        st.error("Error fetching data from The Odds API")
        return pd.DataFrame()
    
    data = response.json()
    
    games = []
    for game in data:
        team1 = game["home_team"]
        team2 = game["away_team"]
        bookmakers = game.get("bookmakers", [])
        
        if bookmakers:
            odds_data = bookmakers[0].get("markets", [])
            
            moneyline_odds = "N/A"
            spread_odds = "N/A"
            total_odds = "N/A"
            
            for market in odds_data:
                if market["key"] == "h2h":
                    moneyline_odds = market["outcomes"]
                elif market["key"] == "spreads":
                    spread_odds = market["outcomes"]
                elif market["key"] == "totals":
                    total_odds = market["outcomes"]
            
            games.append({
                "Home Team": team1,
                "Away Team": team2,
                "Moneyline Odds": moneyline_odds,
                "Spread Odds": spread_odds,
                "Total (O/U) Odds": total_odds
            })
    
    return pd.DataFrame(games)

# Fetch live NCAA data from The Odds API
ncaa_data = get_sports_odds()

# Display all games
st.write("### All Men's College Basketball Games Today")
st.table(ncaa_data)

st.write("🔹 This dashboard now pulls today's NCAA games and live odds from The Odds API!")

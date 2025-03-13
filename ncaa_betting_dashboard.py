import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import matplotlib.pyplot as plt

# Title
st.title("🏀 College Basketball Betting Dashboard")

# Function to fetch NCAA game data from SportsData.io
def get_sportsdata_ncaa_data():
    API_KEY = "your_api_key_here"  # Replace with your actual SportsData.io API key
    url = "https://api.sportsdata.io/v4/cbb/scores/json/GamesByDate/{today_date}"
    today_date = datetime.today().strftime('%Y-%m-%d')
    headers = {"Ocp-Apim-Subscription-Key": API_KEY}
    
    response = requests.get(url.format(today_date=today_date), headers=headers)
    
    if response.status_code != 200:
        st.error("Error fetching data from SportsData.io")
        return pd.DataFrame()
    
    data = response.json()
    games = []
    for game in data:
        team1 = game["HomeTeam"]
        team2 = game["AwayTeam"]
        score1 = game["HomeTeamScore"] if game["HomeTeamScore"] is not None else "N/A"
        score2 = game["AwayTeamScore"] if game["AwayTeamScore"] is not None else "N/A"
        
        games.append({"Home Team": team1, "Away Team": team2, "Score": f"{score1} - {score2}"})
    
    return pd.DataFrame(games)

# Function to get last 10 game scores for a team
def get_last_10_games(team):
    API_KEY = "your_api_key_here"  # Replace with your actual SportsData.io API key
    url = f"https://api.sportsdata.io/v4/cbb/scores/json/TeamGameStatsBySeason/2024/{team}"
    headers = {"Ocp-Apim-Subscription-Key": API_KEY}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return pd.DataFrame()
    
    data = response.json()
    games = []
    for game in data[:10]:  # Get last 10 games
        date = game["Day"]
        opponent = game["Opponent"]
        result = "Win" if game["Wins"] > 0 else "Loss"
        games.append({"Date": date, "Opponent": opponent, "Result": result})
    
    return pd.DataFrame(games)

# Fetch live NCAA data from SportsData.io
ncaa_data = get_sportsdata_ncaa_data()

# Display all games
st.write("### All Men's College Basketball Games Today")
st.table(ncaa_data)

# Display last 10 game results for each team
st.write("### Last 10 Games for Each Team")
if not ncaa_data.empty and "Home Team" in ncaa_data.columns:
    for team in ncaa_data["Home Team"].unique():
        st.write(f"#### {team} - Last 10 Games")
        team_data = get_last_10_games(team)
        st.table(team_data)
        
        # Plot results
        fig, ax = plt.subplots()
        results = team_data["Result"].apply(lambda x: 1 if "Win" in x else 0)  # Convert W/L to binary
        ax.plot(results, marker='o', linestyle='-')
        ax.set_title(f"{team} Last 10 Games Results (1=Win, 0=Loss)")
        ax.set_ylim(-0.5, 1.5)
        st.pyplot(fig)
else:
    st.write("⚠ No game data available. Check SportsData.io API response.")

st.write("🔹 This dashboard now pulls today's NCAA games and last 10 game results from SportsData.io!")

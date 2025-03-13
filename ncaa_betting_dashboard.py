import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import matplotlib.pyplot as plt

# Title
st.title("🏀 College Basketball Betting Dashboard")

# Function to scrape ESPN NCAA data for today's games
def get_espn_ncaa_data():
    today = datetime.today().strftime('%Y%m%d')
    url = f"https://www.espn.com/mens-college-basketball/scoreboard/_/date/{today}"
    headers = {"User-Agent": "Mozilla/5.0"}  # Mimic a real browser request
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    print(response.text)  # DEBUG: Print ESPN HTML response to check if data is retrieved
    
    games = []
    for game in soup.find_all("section", class_="Scoreboard__Item"):  # Updated structure
        teams = game.find_all("div", class_="ScoreCell__TeamName")
        odds = game.find("div", class_="Odds__Container")  # Updated structure
        
        if len(teams) == 2:
            team1 = teams[0].text.strip()
            team2 = teams[1].text.strip()
            odds_text = odds.text.strip() if odds else "N/A"
            
            games.append({"Home Team": team1, "Away Team": team2, "Odds": odds_text})
    
    return pd.DataFrame(games)

# Function to get last 10 game scores for a team
def get_last_10_games(team):
    url = f"https://www.espn.com/mens-college-basketball/team/schedule/_/id/{team}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    games = []
    for row in soup.find_all("tr", class_="Table__TR")[1:11]:  # Extract last 10 games
        cols = row.find_all("td")
        if len(cols) >= 3:
            date = cols[0].text.strip()
            opponent = cols[1].text.strip()
            result = cols[2].text.strip()
            games.append({"Date": date, "Opponent": opponent, "Result": result})
    
    return pd.DataFrame(games)

# Fetch live NCAA data from ESPN
ncaa_data = get_espn_ncaa_data()

# Display all games
st.write("### All Men's College Basketball Games Today")
st.table(ncaa_data)

# Display last 10 game results for each team
st.write("### Last 10 Games for Each Team")
for team in ncaa_data["Home Team"].unique():
    st.write(f"#### {team} - Last 10 Games")
    team_data = get_last_10_games(team)
    st.table(team_data)
    
    # Plot results
    fig, ax = plt.subplots()
    results = team_data["Result"].apply(lambda x: 1 if "W" in x else 0)  # Convert W/L to binary
    ax.plot(results, marker='o', linestyle='-')
    ax.set_title(f"{team} Last 10 Games Results (1=Win, 0=Loss)")
    ax.set_ylim(-0.5, 1.5)
    st.pyplot(fig)

st.write("🔹 This dashboard now pulls today's NCAA games and live odds from ESPN, plus last 10 game results for each team!")

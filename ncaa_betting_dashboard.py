import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import matplotlib.pyplot as plt

# Title
st.title("🏀 College Basketball Betting Dashboard")

# Function to scrape ESPN NCAA data
def get_espn_ncaa_data():
    today_date = datetime.today().strftime('%Y%m%d')
    url = f"https://www.espn.com/mens-college-basketball/scoreboard/_/date/{today_date}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    games = []
    for game in soup.find_all("article", class_="scoreboard" ):
        teams = game.find_all("span", class_="sb-team-short")
        scores = game.find_all("div", class_="score-container")
        
        if len(teams) == 2 and len(scores) == 2:
            team1 = teams[0].text.strip()
            team2 = teams[1].text.strip()
            score1 = scores[0].text.strip()
            score2 = scores[1].text.strip()
            
            games.append({"Home Team": team1, "Away Team": team2, "Score": f"{score1} - {score2}"})
        
        print(response.text)  # DEBUG: Print ESPN HTML response
    
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
if not ncaa_data.empty and "Home Team" in ncaa_data.columns:
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
else:
    st.write("⚠ No game data available. Check ESPN scraping function.")

st.write("🔹 This dashboard now pulls today's NCAA games and last 10 game results from ESPN!")

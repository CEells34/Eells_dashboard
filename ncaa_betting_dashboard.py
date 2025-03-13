import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import matplotlib.pyplot as plt

# Title
st.title("🏀 College Basketball Betting Dashboard")

# Function to scrape Google search results for NCAA games
def get_google_ncaa_data():
    query = "NCAA basketball scores today"
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}  # Mimic a real browser request
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    print(response.text)  # DEBUG: Print Google HTML response to check if data is retrieved
    
    games = []
    for game in soup.find_all("div", class_="BNeawe deIvCb AP7Wnd"):  # Adjust based on Google's structure
        teams = game.find_all("div", class_="BNeawe s3v9rd AP7Wnd")
        scores = game.find_all("div", class_="BNeawe tAd8D AP7Wnd")
        
        if len(teams) == 2 and len(scores) == 2:
            team1 = teams[0].text.strip()
            team2 = teams[1].text.strip()
            score1 = scores[0].text.strip()
            score2 = scores[1].text.strip()
            
            games.append({"Home Team": team1, "Away Team": team2, "Score": f"{score1} - {score2}"})
    
    return pd.DataFrame(games)

# Function to get last 10 game scores for a team
def get_last_10_games(team):
    query = f"{team} last 10 games NCAA basketball"
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    games = []
    for row in soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd")[1:11]:  # Adjust based on Google's structure
        text = row.text.strip()
        games.append({"Game": text})
    
    return pd.DataFrame(games)

# Fetch live NCAA data from Google
ncaa_data = get_google_ncaa_data()

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
    results = team_data["Game"].apply(lambda x: 1 if "W" in x else 0)  # Convert W/L to binary
    ax.plot(results, marker='o', linestyle='-')
    ax.set_title(f"{team} Last 10 Games Results (1=Win, 0=Loss)")
    ax.set_ylim(-0.5, 1.5)
    st.pyplot(fig)

st.write("🔹 This dashboard now pulls today's NCAA games and last 10 game results from Google!")

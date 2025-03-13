import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Title
st.title("🏀 College Basketball Betting Dashboard")

# Sidebar for user input
st.sidebar.header("Game Selection")
selected_team = st.sidebar.text_input("Enter a Team Name:")

# Function to scrape ESPN NCAA data for today's games
def get_espn_ncaa_data():
    today = datetime.today().strftime('%Y%m%d')
    url = f"https://www.espn.com/mens-college-basketball/scoreboard/_/date/{today}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    games = []
    for game in soup.find_all("article", class_="scoreboard" ):
        teams = game.find_all("span", class_="sb-team-short")
        odds = game.find_all("div", class_="odds-details")
        
        if len(teams) == 2:
            team1 = teams[0].text.strip()
            team2 = teams[1].text.strip()
            
            # Extract odds if available
            if odds:
                odds_text = odds[0].text.strip()
            else:
                odds_text = "N/A"
            
            games.append({"Team": team1, "Opponent": team2, "Current Odds": odds_text, "Opening Odds": "Fetching...", "Line Movement": "Calculating..."})
    
    return pd.DataFrame(games)

# Function to scrape opening odds from Vegas Insider
def get_opening_odds():
    url = "https://www.vegasinsider.com/college-basketball/odds/las-vegas/"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    
    opening_odds = {}
    for row in soup.find_all("tr", class_="viOddsLineRow" ):
        columns = row.find_all("td")
        if len(columns) >= 3:
            team_name = columns[0].text.strip()
            opening_line = columns[1].text.strip()
            opening_odds[team_name] = opening_line
    
    return opening_odds

# Fetch live NCAA data from ESPN
ncaa_data = get_espn_ncaa_data()

# Fetch opening odds
opening_odds = get_opening_odds()

# Ensure "Opening Odds" column exists before merging
if not opening_odds:
    ncaa_data["Opening Odds"] = "N/A"
else:
    ncaa_data["Opening Odds"] = ncaa_data["Team"].map(opening_odds).fillna("N/A")

# Calculate line movement
for index, row in ncaa_data.iterrows():
    try:
        opening = float(row["Opening Odds"].replace("+", "")) if row["Opening Odds"] != "N/A" else None
        current = float(row["Current Odds"].replace("+", "")) if row["Current Odds"] != "N/A" else None
        
        if opening and current:
            movement = current - opening
            ncaa_data.at[index, "Line Movement"] = f"{movement:+}"
        else:
            ncaa_data.at[index, "Line Movement"] = "N/A"
    except:
        ncaa_data.at[index, "Line Movement"] = "Error"

# Display filtered results
if selected_team:
    filtered_df = ncaa_data[ncaa_data["Team"].str.contains(selected_team, case=False, na=False)]
    st.write(f"### Games Today for {selected_team}")
    st.table(filtered_df)
else:
    st.write("### All Men's College Basketball Games Today")
    st.table(ncaa_data)

st.write("🔹 This dashboard now pulls today's NCAA games, live odds, and tracks line movement from ESPN & Vegas Insider!")

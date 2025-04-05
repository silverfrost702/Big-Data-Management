# STEP 1: I ran -> pip install pandas pymongo , to connect with mongodb from vscode terminal
from pymongo import MongoClient
import pandas as pd

client = MongoClient('mongodb://localhost:27017/')
db = client["SOCCER"]

#STEP 2: Load data from CSVs into pandas DataFrames
country_df = pd.read_csv('Country.csv')
player_stats_df = pd.read_csv('Player_Assists_Goals.csv')
player_cards_df = pd.read_csv('Player_Cards.csv')
match_results_df = pd.read_csv('Match_results.csv')
players_df = pd.read_csv('players.csv')
wchistory_df = pd.read_csv('WCHistory.csv')  # world_cup_history file

# Step 3: Inserting the COUNTRY documents
for _, row in country_df.iterrows():
    country = {
        "Cname": row['CountryName'],
        "Capital": row['capital'],
        "Population": row['population'],
        "Manager": row['coach'],
        "players": [],
        "WCHistory": []
    }

    # Add players data from players_df based on country
    players_in_country = players_df[players_df['Country'] == row['CountryName']]
    for _, player_row in players_in_country.iterrows():
        yellow_cards = 0
        red_cards = 0
        goals = 0
        assists = 0
        
        # Safely fetch player card information if exists
        player_cards = player_cards_df[player_cards_df['PID'] == player_row['PID']]
        if not player_cards.empty:
            yellow_cards = int(player_cards['no_of_yellow_cards'].values[0])  
            red_cards = int(player_cards['no_of_red_cards'].values[0])  
        
        # Safely fetch player stats (goals and assists) if exists
        player_stats = player_stats_df[player_stats_df['PID'] == player_row['PID']]
        if not player_stats.empty:
            goals = int(player_stats['goals'].values[0])  
            assists = int(player_stats['assists'].values[0])  

        # Create the player document
        player = {
            "Lname": player_row['Lname'],
            "Fname": player_row['Fname'],
            "Height": player_row['Height'],
            "DOB": player_row['BirthDate'],
            "is_Captain": player_row['isCaptain'],
            "Position": player_row['Position'],
            "no_Yellow_cards": yellow_cards,
            "no_Red_cards": red_cards,
            "no_Goals": goals,
            "no_Assists": assists
        }
        country['players'].append(player)

    # Add World Cup history from WCHistory_df based on country
    wc_history = wchistory_df[wchistory_df['Winner'] == row['CountryName']]
    for _, wc_row in wc_history.iterrows():
        wc = {
            "Year": wc_row['Year'],
            "Host": wc_row['Host']
        }
        country['WCHistory'].append(wc)

    # Insert country document into MongoDB
    db.COUNTRY.insert_one(country)

# Step 4: Inserting the STADIUM documents
for _, row in match_results_df.iterrows():
    match = {
        "Stadium": row['stadium'],
        "city": row['city'],
        "matches": []
    }

    # Add match data from match_results_df
    match_data = {
        "Match": {
            "Team1": row['team1'],
            "Team2": row['team2'],
            "Team1Score": int(row['score1']),  
            "Team2Score": int(row['score2']),  
            "Date": row['match_date']
        }
    }
    match['matches'].append(match_data)

    # Insert stadium document into MongoDB
    db.STADIUM.update_one(
        {"Stadium": row['stadium'], "city": row['city']},
        {"$push": {"matches": match_data}},
        upsert=True
    )

print("Data loaded successfully!")

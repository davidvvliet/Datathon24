import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import math
import geopy.distance
import requests
from data_wrangling import *

df = pd.read_csv("datasets/updated_mlb.csv")
coords_df = pd.read_csv("/Users/davidvv/Desktop/DATATHON24/Datathon24/datasets/city_coords.csv")

coords = df_to_coords(coords_df)
# print(coords)
seasons = season_gen(df)

def avg_home_rd(df):
    """
    calculates average home team run differential per season across the data set
    Input:
        df ~ dataframe 
    
    Output:
        avg ~ home team run differential per season across the data set
    """
    return (sum(df["home_score"]) - sum(df["away_score"])) / 690
# avg_home_rd = avg_home_rd(df)


def get_elevation(lat, long):
    query = ('https://api.open-elevation.com/api/v1/lookup'
             f'?locations={lat},{long}')
    r = requests.get(query).json()  
    elevation = pd.io.json.json_normalize(r, 'results')['elevation'].values[0]
    return elevation

def team_avg_rd(df):
    """
    for each season
    When distance is greater than 0, 
        add to some element to store all attributes
        if home team
            home score - away score
        if away team
            away team - home score
    take average run differentials over entire element
    then compare this to run differentials at distances

    Inputs:
        - df = a dataframe
        - team_abbr = a string    run_diff = int()
    """
    avg_travel_rd = defaultdict(int)
    avg_no_travel_rd = defaultdict(int)
    team_numgames = defaultdict(int)
    for _, row in df.iterrows():
        if row["dist_away_team"] > 10: 
            avg_travel_rd[row["away_team"]] += row["home_score"] - row["away_score"]
            team_numgames[row["away_team"]] += 1
            
        if row["dist_home_team"] > 10:
            avg_travel_rd[row["home_team"]] += row["away_score"] - row["home_score"]
            team_numgames[row["home_team"]] += 1

        if row["dist_away_team"] < 10: 
            avg_no_travel_rd[row["away_team"]] += row["home_score"] - row["away_score"]
            team_numgames[row["away_team"]] += 1
            
        if row["dist_home_team"] < 10:
            avg_no_travel_rd[row["home_team"]] += row["away_score"] - row["home_score"]
            team_numgames[row["home_team"]] += 1  
        
    for team, val in avg_travel_rd.items():
            avg_travel_rd[team] = val / team_numgames[team]
            avg_no_travel_rd[team] = val / team_numgames[team]
    return avg_travel_rd, avg_no_travel_rd
    

# print(team_avg_rd(seasons[1]))
# # avrd travel - av rd no travel (true home games) = impact of traveling and accounts for hfa

# # travel_vs_no = np.array(defaultdict{})
# for i in range(23):
#     for team in team_avg_rd(seasons[i])[0]:
#         for team in team_avg_rd(seasons[i])[1]:
#             travel_vs_no[str(team) + str(i)] = team_avg_rd[team][0]- team_avg_rd[team][1]

def distance_to_score(df, coords):
    distances = []
    teams = defaultdict(list)
    all_scorebydist = defaultdict(list)
    
    for _, row in df.iterrows():
        dist = int(round(dist_calc(coords[team_locations[row["away_team"]]], coords[row["city"]]), 0))        
        distances.append(dist)
        net_score = row["away_score"]-row["home_score"]
        all_scorebydist[dist].append(net_score)
        teams[row["away_team"]].append(tuple([dist, net_score]))

    teams_dist = {}
    teams_score = {}
    for team, val in teams.items():
        teams[team].sort(key=lambda x: x[0])
        teams_dist[team] = [i[0] for i in val]
        teams_score[team] = [i[1] for i in val]

    

    avg_scorebydist = []
    for team, val in all_scorebydist.items():
        avg_scorebydist.append(tuple([team, sum(val)/len(val)]))
    avg_scorebydist.sort(key=lambda x: x[0])
    print(avg_scorebydist)

    return teams, teams_dist, teams_score, all_scorebydist, avg_scorebydist



coords = coord_mapping(df)
teams, teams_dist, teams_score, all_scorebydist, avg_scorebydist = distance_to_score(df, coords)
# print(teams)
teams_col = []
# for team, val in teams.keys():
#     for _ in range(len(val)):
#         teams_col.append(teams)
# away_games_score = pd.DataFrame(teams_col, [x[0] for x in teams.values()])

plt.plot([x[0] for x in avg_scorebydist], [x[1] for x in avg_scorebydist])
plt.show()

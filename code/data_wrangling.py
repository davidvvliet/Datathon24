import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import math
import geopy.distance
import requests
from timezonefinder import TimezoneFinder 


df = pd.read_csv("~/Desktop/DATATHON24/Datathon24/datasets/datathon_2024_dataset_corrected.csv")
df_world = pd.read_csv("/Users/davidvv/Desktop/DATATHON24/Datathon24/datasets/worldcities.csv")
coords_df = pd.read_csv("/Users/davidvv/Desktop/DATATHON24/Datathon24/datasets/city_coords.csv")

def filter_by_year(df, start_date, end_date):
    """
    Inputs:
        - df = a dataframe of all the games data
        - start_date = in yyyymmdd format: the first possible date of games to be part of the array
        - end_date = in yyyymmdd format: the last possible date of games to be part of the array
    Returns:
        - an array containing all the games in the date range provided
    """
    filtered_df = df[(df['game_date'] >= int(start_date)) & (df['game_date'] <= int(end_date))]
    return filtered_df

def season_gen(df):
    """
    Produces a dictionary that has the year as a key and 
        an array of all the games from that year as values
    Inputs:
        - df = a dataframe of all the games data
    Returns:
        - a dictionary that has the year as a key and an array of all the games from that year as values
    """
    seasons = {}
    for i in range(23):
        lb = str(i) if i >= 10 else ("0" + str(i))
        ub = str(i+1) if i >= 9 else ("0" + str(i+1))
        seasons[i] = filter_by_year(df, "20" + lb + "0000", "20" + ub + "0000")
    return seasons

# seasons = season_gen(df)



def diff_gen(season):
    """
    Calculates the score differential for a season for each team

    Input:
        - season, a df containing the data from a specific season
    Output:
        - score_df, a mapping from teams to an array of size two containing the
          score differentials 
    """
    score_diff = {}
    for _, row in season.iterrows():
        score_diff[row["home_team"]] = [0, 0]
        score_diff[row["away_team"]] = [0, 0]
    for _, row in season.iterrows():
        score_diff[row["home_team"]][0] += row["home_score"]-row["away_score"]
        score_diff[row["away_team"]][1] += row["away_score"]-row["home_score"]
    return score_diff

# all_seasons_diff = []  
# for val in seasons.values():
#     all_seasons_diff.append(diff_gen(val))

#print(all_seasons_diff)


#def team_h_vs_a(team_abbr, all_seasons_diff):
    """
    Calculates difference between the home run differential and away run differential
    Inputs:
        - team_abbr = abbreviation of team name that you want to run
    Returns:
        - difference between home and away run differential
    """
   # home_minus_away= {}
   # for i in range(690):
   #     home_minus_away["team_abbr" + str(i)] = all_seasons_diff[i][0] - all_seasons_diff[i][1]
   # return home_minus_away

state_mapping = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'DC': 'District of Columbia',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming',
    'JAP': 'Japan',
    'QUE': 'Quebec',
    'PR': 'Puerto Rico',
    'MX': 'Mexico',
    'England': 'United Kingdom',
    'ONT': "Ontario",
    'Australia': 'Australia'
}

def coord_mapping(df):
    area = []
    for state in df["state"]:
        area.append(state_mapping[state])
    city_state = set(list(zip(df["city"], area)))
    coords = {}
    for _, row in df_world.iterrows():
        for place in city_state:
            if row["country"] in ["Canada", "United States"]:
                if row["city_ascii"] == place[0] and row["admin_name"] == place[1]:
                    latlng = tuple([row["lat"], row["lng"]])
                    coords[row["city_ascii"]] = latlng
            else:
                if row["city_ascii"] == place[0] and row["country"] == place[1]:
                    latlng = tuple([row["lat"], row["lng"]])
                    coords[row["city_ascii"]] = latlng
    # print(coords, len(coords))
    
    return coords

# def coords_to_df(coords):
#     df = pd.DataFrame(list(zip(coords.keys(), coords.values())), columns=["city", "coords"])
#     df.to_csv("datasets/city_coords.csv")
# coords_to_df(coord_mapping(df))
# coords = coord_mapping(df)
# print(coords, len(coords))
# print(len(coords))

# Fort Bragg = Fayetteville
# Lake Buena Vista = Celebration
# Dyersville = Dubuque

team_locations = {
    "ATL" : "Atlanta",
    "BAL" : "Baltimore",
    "TBA" : "St. Petersburg",
    "ARI" : "Phoenix",
    "CIN" : "Cincinnati",
    "CHN" : "Chicago",
    "COL" : "Denver",
    "PHI" : "Philadelphia",
    "WAS" : "Washington",
    "SFN" : "San Francisco",
    "KCA" : "Kansas City",
    "MIL" : "Milwaukee",
    "FLO" : "Miami",
    "MIA" : "Miami",
    "SLN" : "St. Louis",
    "NYN" : "New York",
    "NYA" : "New York",
    "CLE" : "Cleveland",
    "LAN" : "Los Angeles",
    "SDN" : "San Diego",
    "SEA" : "Seattle",
    "TEX" : "Arlington",
    "MON" : "Montreal",
    "CHA" : "Chicago",
    "DET" : "Detroit",
    "PIT" : "Pittsburgh",
    "MIN" : "Minneapolis",
    "HOU" : "Houston", 
    "ANA" : "Anaheim", 
    "OAK" : "Oakland", 
    "TOR" : "Toronto", 
    "BOS" : "Boston"
}

time_zone_number = {
    "America/New_York" : 0,
    "America/Chicago" : -1,
    "America/Denver" : -2,
    "America/Phoenix" : -3,
    "America/Los_Angeles" : -3,
    "Asia/Tokyo" : 13,
    "America/Monterrey" : -2,
    "America/Mexico_City": -2,
    "America/Puerto_Rico": -2,
    "America/Toronto" : 0,
    "Europe/London" : 4,
    "Australia/Sydney" : 16,
}


def dist_calc(coord1, coord2):
    '''
    Calculates the distance between two pairs of latitude and longitude using geopy library
    '''
    
    return geopy.distance.geodesic(coord1, coord2).km
   

obj = TimezoneFinder() 
def find_timezone(lat, lng):
    return obj.timezone_at(lat=coord1,lng= coord2)

def adding_distance_col(df, coords):
    distances_away = []
    distances_home= []
    tmdiff_away = []
    for _, row in df.iterrows():
        coord1, coord2 = coords[team_locations[row["away_team"]]], coords[row["city"]]
        dist = int(round(dist_calc(coord1, coord2), 0))
        dist2 = int(round(dist_calc(coord1, coord2), 0))
        distances_away.append(dist)
        distances_home.append(dist2)
        tmdiff_away.append(abs(find_timezone(coord2[0], coord2[1]) - find_timezone(coord1[0], coord1[1])))

    df.insert(7, "dist_away_team", distances_away, True)
    df.insert(8, "dist_home_team", distances_home, True)
    df.insert(9, "time_diff_away", tmdiff_away, True)
    return df

def df_to_coords(coords_df):
    coords = {}
    for _, row in coords_df.iterrows():
        coords[row["city"]] = row["coords"]
    return coords

coords = df_to_coords(coords_df)


df = adding_distance_col(df,  coords)
# print(df.head(10))
# print(df["dist_away_team"])
# df.to_csv("datasets/updated_mlb.csv")

def get_elevation(lat, long):
    query = ('https://api.open-elevation.com/api/v1/lookup'
             f'?locations={lat},{long}')
    r = requests.get(query).json()  
    elevation = pd.io.json.json_normalize(r, 'results')['elevation'].values[0]
    return elevation
        







# -*- coding: utf-8 -*-
"""

Input - Output Processes for Metrica Data.


@author: Apatsidis Ioannis
"""


import pandas as pd
import numpy as np
import os
import csv


def read_event_data(DATA_DIR : str,game_id : int):
    """
    Reads Event data for game with given game_id.

    Parameters
    ----------
    DATA_DIR: Directory of Data.
    game_id: Id of the game.
    
    Returns
    -------
    event_data_df: Pandas Dataframe with the event data.
    
    """
    
    csv_path=os.path.join(DATA_DIR,"data\Sample_Game_{0}\Sample_Game_{1}_RawEventsData.csv".format(game_id,game_id))
    event_data_df=pd.read_csv(csv_path)
    return event_data_df


def transform_coord_system(df: pd.DataFrame,center_coord=(0.5,0.5),field_dimensions=(106,68)):
    
    """
    Transforms coordinates into meters based on the real dimensions of the field. Default dimensions for the field are 
    105m x 68m. Metrica defines the origin at the top-left of the field (0,0).Now the (0,0) is at 
    the center of the field.
    
    Parameters
    ----------
    df: pandas DataFrame with Event or Tracking Data.
    center_coord: Coordinates of the center of the field before transformation.
    field_dimensions: Field dimensions in meters (Width x Height).
    
    Returns
    -------
    df: Event Dataframe with transformed coordinate system.
    
    """
    x_columns=[col for col in df.columns if col[-1].lower()=="x"] # Columns ending with 'x'
    y_columns=[col for col in df.columns if col[-1].lower()=="y"] # Columns ending with 'y'

    df.loc[:,x_columns]=(df.loc[:,x_columns]-center_coord[0]) * field_dimensions[0]
    df.loc[:,y_columns]=-1*(df.loc[:,y_columns]-center_coord[1]) * field_dimensions[1]

    return df


def set_single_playing_direction(event,tracking_home,tracking_away):
    """
    Reversing coordinates for 1rst Period so that the home team always attacks from left to right, regardless the Period.
    
    Parameters
    ----------
    event: pd.Dataframe with Event Data.
    tracking_home: pd.Dataframe with Tracking Data for Home Team.
    tracking_away: pd.Dataframe with Tracking Data for Away Team.
    
    Returns
    ------
    event,tracking_home,tracking_away: Updated Event and Tracking Data pd.DataFrames.
    """
    
    # Checks if the away team starts from left side of field
    players_away=np.unique(([x.split('_')[0]+'_'+x.split('_')[1] for x in tracking_away.columns if "Away_" in x]))
    left_players_count=0
    for p in players_away:
        if tracking_away.loc[1,p+"_x"]<0:
            left_players_count+=1 # +1 Player in the left of the center line
    
    if left_players_count>7: #Away team starts left side in KICK OFF
        p=1 # Period to reverse is First Period
    else:
        p=2 # Period to reverse is Second Period
    
    for df in [event,tracking_home,tracking_away]:
        xy_columns=[col for col in df.columns if col[-1].lower()=="x" or col[-1].lower()=="y"] # Columns ending with 'x' or 'y'
        df.loc[df["Period"]==p,xy_columns]=df.loc[df["Period"]==p,xy_columns].apply(lambda x: x*(-1)) # Reversing coordinates
        
    return event,tracking_home,tracking_away


def read_tracking_data(DATA_DIR: str,game_id: int , team: str):
    """
    Reads Tracking data for given game_id and team. Bench Players have Nan Values in their x and y positions.
    
    Parameters
    ----------
    DATA_DIR: Directory of Data.
    game_id: Id of the game.
    team: name of team. For sample data acceptable values are "Home", "Away".
    
    Returns
    -------
    tracking_data_df: pd.Dataframe with the tracking data.
    
    """
    
    csv_path =os.path.join(DATA_DIR, "data\Sample_Game_{0}\Sample_Game_{1}_RawTrackingData_{2}_Team.csv".format(game_id,game_id,team))
    #Set Player names from file headers
    csvfile =  open(csv_path, 'r') # create a csv file reader
    reader = csv.reader(csvfile) 
    team_name = next(reader)[3].lower()
    print("Reading team: %s" % team_name)
    # construct column names
    jerseys = [x for x in next(reader) if x != ''] # extract player jersey numbers from second row
    columns = next(reader)
    for i, j in enumerate(jerseys): # create x and y position column headers for each player
        columns[i*2+3] = "{0}_{1}_x".format(team, j)
        columns[i*2+4] = "{0}_{1}_y".format(team, j)
    # column headers for the x and y positions of the ball    
    columns[-2] = "ball_x"
    columns[-1] = "ball_y"
    # Read the tracking Data
    tracking_data_df = pd.read_csv(csv_path, names=columns, index_col='Frame', skiprows=3)
    return tracking_data_df


def get_goalkeeper_name(tracking_team):
    
    '''
    Finds the name of the goalkeeper by checking who's closer to the goal line at KICK OFF (Frame 1).
    Needs single direction transformation.
    
    Parameters
    ----------
    tracking_team: pd.Dataframe with the tracking data.
    
    Returns
    -------
    gk: name of Goalkeeper like "Away_25" or "Home_11"
    '''
    
    
    # Get all players , e.g. Home_1 , Away_2
    players=np.unique(([x.split('_')[0]+'_'+x.split('_')[1] for x in tracking_team.columns if "Away_" in x or "Home_" in x]))
    min_dist=float('inf')
    gk=""
    goal_line_coord=(-68.,0) if "Home" in players[0] else (68.,0)
    # find distance from each player position to goal line
    for p in players:
        dist=np.sqrt(abs(goal_line_coord[0]-tracking_team.loc[1,p+"_x"])+abs(goal_line_coord[1]-tracking_team.loc[1,p+"_y"]))
        if dist<min_dist:
            min_dist=dist
            gk=p
    return gk

def find_attacking_direction(team):
    '''
    Finds attacking direction of given team.
    Requires setting single player direction.
    
    Parameters
    ----------
    team: Name of team. "Home" or "Away".
    
    Returns
    -------
    1: left to right
    -1: right to left
    '''
    
    
    if team=="Home":
        return 1 # 1 indicates attacking from left to right
    elif team=="Away":
        return -1 # -1 indicates attacking from right to left
    else:
        raise Exception("Invalid team name.")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
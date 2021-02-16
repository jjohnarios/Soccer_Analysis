# -*- coding: utf-8 -*-
"""
Inspiration by: Friends-of-Tracking-Data-LaurieOnTracking

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
    
    for df in [event,tracking_home,tracking_away]:
        xy_columns=[col for col in df.columns if col[-1].lower()=="x" or col[-1].lower()=="y"] # Columns ending with 'x' or 'y'
        df.loc[df["Period"]==1,xy_columns]=df.loc[df["Period"]==1,xy_columns].apply(lambda x: x*(-1)) # Reversing coordinates
        
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
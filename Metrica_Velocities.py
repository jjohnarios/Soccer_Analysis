# -*- coding: utf-8 -*-
"""

Inspiration by: Friends-of-Tracking-Data-LaurieOnTracking

@author: Apatsidis Ioannis
"""
import re
import numpy as np


def calc_player_velocities(team,max_speed=11,smoothing=True):
    """
    Calculate player velocities and speed.
    
    Parameters
    ----------
    team: pd.DataFrame with Tracking Data for a team.
    max_speed: Maximum speed that a human is reallistically able to run in meters/second. Speeds higher than this value are considered outliers and set to NaN.
    smoothing: Boolean variable determining if "moving average" is going to be applied to the calculation of velocities
    Returns
    -------
    team: pd.DataFrame with players' xy velocities and speed.
    
    """
    
    team=remove_player_velocities(team)
    
    # Time intervals per measurement in Metrica Data are always 40ms.
    time_intervals=team["Time [s]"].diff()
    
    # Get all players , e.g. Home_1 , Away_2
    players=np.unique(([x.split('_')[0]+'_'+x.split('_')[1] for x in team.columns if "Away_" in x or "Home_" in x]))
    
    team_name=team.columns[3].split("_")[0]
    print("Calculating velocities for: ",team_name )
    
    for player in players:
        
        
        # Add velocities to DataFrame
        team[player+"_vx"]=team[player+"_x"].diff()/time_intervals
        team[player+"_vy"]=team[player+"_y"].diff()/time_intervals
        
        # Excluding Errors in measurements / Unrealistic velocities that exceed the maximun speed
        if (max_speed>0):
            speed_estimate=np.sqrt(team[player+"_vx"]**2 + team[player+"_vy"]**2)
            team.loc[speed_estimate>max_speed,player+"_vx"]=np.nan
            team.loc[speed_estimate>max_speed,player+"_vy"]=np.nan
            
        # Apply Moving Average for smoothing
        # mode='same' means same as before smoothing when there are no 5(window) points, same length.
        if (smoothing):
            window=5
            box=np.ones(window)/window # Adding 5 and divide by 5.
            team[player+"_vx"]=np.convolve(team[player+"_vx"],box,mode="same")
            team[player+"_vy"]=np.convolve(team[player+"_vy"],box,mode="same")
            
        # Add speed to DataFrame (m/s)
        team[player+"_speed"]=np.sqrt(team[player+"_vx"]**2 +team[player+"_vy"]**2)

    
    
    return team



def remove_player_velocities(team):
    """
    Remove already calculated velocities and speed.
    
    Parameters
    ---------
    team: pd.DataFrame with tracking data of a team.
    
    Returns
    -------
    team: Updated team pd.DataFrame.
    
    """
    
    # Either end with _vx or _vy or _speed
    velocity_columns=[x for x in team.columns if re.match(r".*_vx$|.*_vy$|.*_speed$",x)]
    team.drop(velocity_columns,axis='columns',inplace=True)
    return team





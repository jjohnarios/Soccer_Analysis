# -*- coding: utf-8 -*-
"""
Inspiration by: Friends-of-Tracking-Data-LaurieOnTracking

@author: Apatsidis Ioannis
"""

import Metrica_Velocities as mvel
import numpy as np
import pandas as pd

def get_players_summary(team):
    
    '''
    
    Calculates summary performance metrics for each player of the given team:
    ["Minutes Played","Distance (km)","Walking (km)","Jogging (km)","Running (km)","Sprinting (km)","# of Sprints"]
    
    Parameters
    ----------
    team: pd.DataFrame of Tracking data for teams' players. 
    
    Returns
    -------
    summary: pd.DataFrame with summary performance metrics for teams' players.
    
    '''
    
    # Velocities are necessary for calculations
    if not (any("_speed" in col for col in team.columns)):
        print("Velocities need to be calculated for summary")
        team=mvel.calc_player_velocities(team)
    
    # Creating the Summary DataFrame
    player_indices=np.unique([x[:-2] for x in team.columns if x[-2:]=='_x' and 'ball' not in x])
    columns=["Minutes Played","Distance (km)","Walking (km)","Jogging (km)","Running (km)","Sprinting (km)","# of Sprints"]
    summary=pd.DataFrame(index=player_indices,columns=columns)
    
    
    # Sprint thresholds for calculating # of continous sprints
    speed_threshold=7 # Sprinting when: 7 m/s <= speed
    time_threshold=25 # Sprinting for at least 25 frames (1 sec)
    
    
    for player in player_indices:
         
        # Calculating Minutes Played
        first_frame=team.loc[~pd.isna(team[player+"_x"]),"Time [s]"].min()
        last_frame=team.loc[~pd.isna(team[player+"_x"]),"Time [s]"].max()
        
        # Seconds into minutes
        summary.loc[player,"Minutes Played"]=(last_frame-first_frame)/60
        
        
        # Calculating Distance       
        summary.loc[player,"Distance (km)"]=(team[player+"_speed"].sum()*0.04)/1000 # Sample every 0.04 ms
        
        
        # SETTING THRESHOLDS based on average athletes
        # Walking when : speed < 2 m/s
        summary.loc[player,"Walking (km)"]=(team.loc[team[player+"_speed"]<2,player+"_speed"].sum()*0.04)/1000
        # Jogging when : 2 m/s <= speed < 4 m/s
        summary.loc[player,"Jogging (km)"]=(team.loc[(team[player+"_speed"]>=2) & (team[player+"_speed"]<4),player+"_speed"].sum()*0.04)/1000
        # Running when : 4 m/s <= speed < 7 m/s
        summary.loc[player,"Running (km)"]=(team.loc[(team[player+"_speed"]>=4) & (team[player+"_speed"]<7),player+"_speed"].sum()*0.04)/1000 
        # Sprinting when: 7 m/s <= speed
        summary.loc[player,"Sprinting (km)"]=(team.loc[team[player+"_speed"]>=7,player+"_speed"].sum()*0.04)/1000
        
        
        # Calculating # of sprints
        
        # Convolution of speed with time_threshold window
        # Convolution to get the number of consecutive frames
        conv=np.convolve(1*(team[player+"_speed"]>=speed_threshold),np.ones(time_threshold),mode='same')
        # Set 1 where cell>=time_threshold consecutive frames
        player_sprints=np.diff(1*(conv>=time_threshold))
        # Adding all the 1's that represent a continous sprint
        summary.loc[player,"# of Sprints"]=np.sum(player_sprints==1)
                    
        '''
        e.g. time_threshold=5 , speed_threshold=7
        
        convolution of ( [0,0,1,1,1,0,1,1,1,1,1],[1,1,1,1,1] ,mode='same') -> [0,0,1,2,3,3,4,4,4,4,5,4,3,2,1]
                                      sprint no1
        5 indicates that there is 5 concecutive 1's which means 5 concecutive speeds > speed_threshold
        
        player_sprints= 0,  0,  0,  0,  0,  0,  0,  0,  0,  1, -1,  0,  0,  0] , 1 indicates a sprint
        
        np.sum(player_sprints==1) : # of sprints
        '''

    
    return summary
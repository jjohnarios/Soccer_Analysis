# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 20:28:16 2021


Inspiration by: Friends-of-Tracking-Data-FoTD/LaurieOnTracking

@author: Apatsidis Ioannis
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mat
import re


def plot_pitch(field_dimensions=(106.,68.)) :
    """
    Visual represantation of Pitch based on given coordinates in Meters.
    
    Parameters
    ----------
    field_dimensions:  Field dimensions in meters (Width x Height).
    
    Returns
    -------
    fig,ax : Figure and Axis objects of the Pitch plot
    """
    
    
    half_field_length=field_dimensions[0]/2
    half_field_width=field_dimensions[1]/2
    
    fig= plt.figure(figsize=(10,8))
    ax=plt.gca()
    
    # Setting ticks 
    plt.xticks(np.arange(-half_field_length-10,half_field_length+10,1))
    plt.yticks(np.arange(-half_field_width-10,half_field_width+10,1))
    
    # Based on Pitch dimensions found on the Internet in yards.
    meters_per_yard=0.9144
    goal_height=3*meters_per_yard
    penalty_spot=12*meters_per_yard
    goal_line_width = 8*meters_per_yard
    goal_area_width = 20*meters_per_yard
    goal_area_length = 6*meters_per_yard
    area_width = 44*meters_per_yard
    area_length = 18*meters_per_yard
    penalty_spot = 12*meters_per_yard
    corner_radius = 1*meters_per_yard
    center_circle_radius = 10*meters_per_yard
    goal_box_line_length=6*meters_per_yard # Length(and width) between Goal and box
    dots_radius=0.2
    
    # Kick off
    center_dot=plt.Circle((0,0),dots_radius,color='b')
    center_circle=plt.Circle((0,0),center_circle_radius,color='b',fill=False)
    center_line=plt.Line2D(np.array([0,0]),np.array([-half_field_width,half_field_width]),color='b')
    
    # Penalty spots
    left_penalty_spot=plt.Circle((-half_field_length+penalty_spot,0),dots_radius,color='b')
    right_penaly_spot=plt.Circle((half_field_length-penalty_spot,0),dots_radius,color='b')
    
    #Border lines
    bottom_touchline=plt.Line2D(np.array([-half_field_length,half_field_length]),np.array([-half_field_width,-half_field_width]),color='b')
    top_touchline=plt.Line2D(np.array([-half_field_length,half_field_length]),np.array([half_field_width,half_field_width]),color='b')
    left_goal_line=plt.Line2D(np.array([-half_field_length,-half_field_length]),np.array([-half_field_width,half_field_width]),color='b')
    right_goal_line=plt.Line2D(np.array([half_field_length,half_field_length]),np.array([-half_field_width,half_field_width]),color='b')
    
    # Penalty areas
    left_penalty_area=plt.Rectangle((-half_field_length,-area_width/2),area_length,area_width,edgecolor='b',facecolor='none')
    right_penalty_area=plt.Rectangle((half_field_length-area_length,-area_width/2),area_length,area_width,edgecolor='b',facecolor='none')
    
    # Goal area
    left_goal_area=plt.Rectangle((-half_field_length,-goal_line_width/2-goal_box_line_length),goal_area_length,goal_area_width,edgecolor='b',facecolor='none')
    right_goal_area=plt.Rectangle((half_field_length-goal_box_line_length,-goal_line_width/2-goal_box_line_length),goal_area_length,goal_area_width,edgecolor='b',facecolor='none')

    # Semicircles outside penalty area
    left_semicircle=mat.patches.Arc((-half_field_length+area_length,0),8*meters_per_yard,10*meters_per_yard,theta1=270,theta2=450,color='b')
    right_semicircle=mat.patches.Arc((half_field_length-area_length,0),8*meters_per_yard,10*meters_per_yard,theta1=90,theta2=270,color='b')

    # Corners
    left_bottom_corner=mat.patches.Polygon(np.array([[-half_field_length,-half_field_width],[-half_field_length,-half_field_width+corner_radius],[-half_field_length+corner_radius,-half_field_width]]),closed=True,facecolor='None',edgecolor='b')
    left_top_corner=mat.patches.Polygon(np.array([[-half_field_length,half_field_width],[-half_field_length+corner_radius,half_field_width],[-half_field_length,half_field_width-corner_radius]]),closed=True,facecolor='None',edgecolor='b')
    right_top_corner=mat.patches.Polygon(np.array([[half_field_length,half_field_width],[half_field_length,half_field_width-corner_radius],[half_field_length-corner_radius,half_field_width]]),closed=True,facecolor='None',edgecolor='b')
    right_bottom_corner=mat.patches.Polygon(np.array([[half_field_length,-half_field_width],[half_field_length,-half_field_width+corner_radius],[half_field_length-corner_radius,-half_field_width]]),closed=True,facecolor='None',edgecolor='b')
    
    # Goal
    left_goal=plt.Rectangle((-half_field_length-goal_height,-goal_line_width/2),goal_height,goal_line_width,edgecolor='b',facecolor='none')
    right_goal=plt.Rectangle((half_field_length,-goal_line_width/2),goal_height,goal_line_width,edgecolor='b',facecolor='none')
    
    # Pitch Borders (+/- 5 Meters)
    pitch=plt.Rectangle((-half_field_length-5,-half_field_width-5),2*half_field_length+10,2*half_field_width+10,facecolor='#32CD32')
    ax.add_patch(pitch) 

    # Grouping objects
    lines=[center_line,bottom_touchline,top_touchline,left_goal_line,right_goal_line]
    patches=[center_dot,center_circle,left_penalty_spot,right_penaly_spot,left_penalty_area,right_penalty_area,left_goal_area,right_goal_area,
             left_semicircle,right_semicircle,left_bottom_corner,left_top_corner,right_top_corner,right_bottom_corner,left_goal,right_goal]
    
    for patch in patches:
        ax.add_patch(patch)
    
    for line in lines:
        ax.add_line(line)
    
   # Setting green background color and droping axis
   # fig.patch.set_facecolor('#32CD32')
    plt.axis('off')
    #plt.show()
    
    return fig,ax
    

def plot_events(events,figax=None,field_dimensions=(106.,68.),color='r',alpha=0.6,marker='o',annotate_player=False,annotate_turn=False):
    """
    Plots a series of events.
    
    Parameters
    ---------
    events: pd.DataFrame containing events.
    figax: Figure, Axis object of an existing pitch. Default is None.
    field_dimensions:  Field dimensions in meters (Width x Height). Default is (106,68).
    color: color of indicator. Default is 'r' (red).
    alpha: alpha of event marker.Default=0.6.
    marker: marker of event posistion. Default is 'o'.
    annotate_player: Annotate Player. E.g. Player 1 -> P1. Default is False.
    annotate_turn: Annotate turn of events.
    
    Returns
    ------
    fig,ax : Figure , Axis onbjects of the plot.
    
    """
    
    if figax==None: #create new pitch
        fig,ax=plot_pitch(field_dimensions=field_dimensions)
    else: # overlay on existing pitch
        fig,ax=figax
    
    turns=1 # Indicate the series of the events.
    
    for stX,stY,endX,endY,player,to in events.loc[:,["Start X","Start Y","End X","End Y","From","To"]].to_numpy():
        
        
        if annotate_turn:
            ax.text(field_dimensions[0]/2-40,field_dimensions[1]/2+10,"e.g. '1:P2' -> 1rst Event from Player 2.",fontsize=10,bbox=dict(facecolor='#3C83F6', alpha=0.5,edgecolor='blue'), va = "top", ha="left")
            annotate=str(turns)+": "
        else:
            annotate=""

        if annotate_player:# Annotate name of Player and little helper box.
            annotate+=player.replace("Player","P")
        
        ax.plot(stX,stY,marker=marker,color=color)
        ax.annotate(annotate,xy=(endX,endY),xytext=(stX,stY), alpha=alpha, arrowprops=dict(arrowstyle="->",color=color))
        
        
        if not(to!=to): # Only increment when To is not nan
            turns+=1
    return fig,ax
    

    
def plot_frame(home_series,away_series,field_dimensions=(106.,68.),figax=None,home_team_color='black',away_team_color='red',marker='o',annotate_player=False):
    """
    Plots a frame with the positions of all the players and the ball in the field.All distances should be in meters.
    
    Parameters
    ----------
    home_series: pd.Series containing tracking data for the given frame.
    away_series: pd.Series containing tracking data for the given frame.
    figax: Figure, Axis object of an existing pitch.Default is None.
    home_team_color: Color of home team. Default is 'black'.
    away_team_color: Color of away team. Default is 'red'.
    field_dimensions:  Field dimensions in meters (Width x Height). Default is (106,68).
    marker: marker of event posistion. Default is 'o'.
    annotate_player: Annotate Player. Default is False.
    
    Returns
    -------
    fig,ax : Figure , Axis onbjects of the frame plot.
    
    """
    
    if figax==None: #create new pitch
        fig,ax=plot_pitch(field_dimensions=field_dimensions)
    else: # overlay on existing pitch
        fig,ax=figax
        
    # Get Players' x and y coordinates    
    home_player_colums=[x for x in home_series.index if (re.match(r"Home_[0-9]+_[x|y]",x))]
    away_player_colums=[x for x in away_series.index if (re.match(r"Away_[0-9]+_[x|y]",x))]

    for i in range(len(home_player_colums)-1):
        
        # Skip double passing
        if i%2!=0:
            continue
        
        if annotate_player:# Annotate name of Player for Home Team
            annotate_home="P"+home_player_colums[i].split("_")[1]
        else:
            annotate_home=""
            
        # Plot one player from home team    
        ax.plot(home_series[home_player_colums[i]],home_series[home_player_colums[i+1]],marker=marker,color=home_team_color)
        ax.annotate(annotate_home,xy=(home_series[home_player_colums[i]],home_series[home_player_colums[i+1]]),color=home_team_color)
        
        
    for i in range(len(away_player_colums)-1):
        
        # Skip double passing
        if i%2!=0:
            continue
        
        if annotate_player:# Annotate name of Player for Away Team
            annotate_away="P"+away_player_colums[i].split("_")[1]
        else:
            annotate_away=""
            
        # Plot one player from away team    
        ax.plot(away_series[away_player_colums[i]],away_series[away_player_colums[i+1]],marker=marker,color=away_team_color) 
        ax.annotate(annotate_away,xy=(away_series[away_player_colums[i]],away_series[away_player_colums[i+1]]),color=away_team_color)
    
    # Plot the ball
    ax.plot(home_series["ball_x"],home_series["ball_y"],marker=marker,markersize=3,color='white')
    
    return fig,ax



















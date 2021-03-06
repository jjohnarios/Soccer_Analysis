# -*- coding: utf-8 -*-
"""
Visualization plots and clips.

@author: Apatsidis Ioannis
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mat
import re
import matplotlib.animation as animation
import os
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.colors 
import Metrica_IO as mio


def plot_pitch(field_dimensions=(106.,68.),field_color="#32CD32",alpha=0.8) :
    """
    Visual represantation of Pitch based on given coordinates in Meters.
    
    Parameters
    ----------
    field_dimensions:  Field dimensions in meters (Width x Height).
    field_color: Field color. Default is '#32CD32'(light green).
    alpha: alpha of background color.
    
    Returns
    -------
    fig,ax : Figure and Axis objects of the Pitch plot
    """
    
    
    half_field_length=field_dimensions[0]/2
    half_field_width=field_dimensions[1]/2
    
    fig,ax= plt.subplots(figsize=(10,8))
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
    pitch=plt.Rectangle((-half_field_length-5,-half_field_width-5),2*half_field_length+10,2*half_field_width+10,facecolor=field_color,alpha=0.2)
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
            annotate_text=str(turns)+": "
        else:
            annotate_text=""

        if annotate_player:# Annotate name of Player and little helper box.
            annotate_text+=player.replace("Player","P")
        
        ax.plot(stX,stY,marker=marker,color=color)
        if not np.isnan(stX): # nan -> infinite for ax.text
            ax.text(stX,stY,annotate_text,color='k', weight='bold')
            turns+=1
        ax.annotate("",xy=(endX,endY),xytext=(stX,stY), alpha=alpha, arrowprops=dict(arrowstyle="->",color=color))
        
        
            
    return fig,ax
    

    
def plot_frame(home_series,away_series,include_player_velocities=False,field_dimensions=(106.,68.),figax=None,home_team_color='black',away_team_color='red',ball_color="white",marker='o',annotate_player=False,player_alpha=0.7,markersize=3):
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
    include_player_velocities: Shows velocities of players. Default is False.
    player_alpha: Alpha. Default is 0.7
    
    Returns
    -------
    fig,ax : Figure , Axis objects of the frame plot.
    
    """
    
    if figax==None: #create new pitch
        fig,ax=plot_pitch(field_dimensions=field_dimensions)
    else: # overlay on existing pitch
        fig,ax=figax
        
    for team,color in zip([home_series,away_series],[home_team_color,away_team_color]):
        x_columns=[x for x in team.index if 'ball' not in x and x[-2:].lower()=='_x']
        y_columns=[y for y in team.index if 'ball' not in y and y[-2:].lower()=='_y']
        ax.plot(team[x_columns], team[y_columns], marker,color=color, alpha=player_alpha )
        if include_player_velocities:
            vx_columns=[x.replace("_x","_vx") for x in x_columns]
            vy_columns=[y.replace("_y","_vy") for y in y_columns]
            ax.quiver( team[x_columns], team[y_columns], team[vx_columns], team[vy_columns], color=color, scale_units='inches', scale=10,width=0.0025,headlength=5,headwidth=3,alpha=1,zorder=2)
            
        if annotate_player:
            [ ax.text( team[x]+0.5, team[y]+0.5, x.split('_')[1], fontsize=10, color=color  ) for x,y in zip(x_columns,y_columns) if not ( np.isnan(team[x]) or np.isnan(team[y]) ) ] 
            
    # Plot the ball
    ax.plot(home_series["ball_x"],home_series["ball_y"],marker=marker,markersize=markersize,color=ball_color)
    
    return fig,ax



def save_movie(tracking_home,tracking_away,file_path,file_name,fps=25,figax=None, field_dimensions = (106.0,68.0),include_player_velocities=False,home_team_color='black',away_team_color='red',marker='o',player_alpha=0.7):
    """
    Saves a movie based on the given indices of Tracking Data. It saves the file in file_path with name as the filename.mp4.
    Indices must be the same for tracking_home and tracking_away.
    
    Parameters
    ----------
    tracking_home: pd.DataFrame with Tracking Data for Home team.
    tracking_away: pd.DataFrame with Tracking Data for Away team.
    file_path: Path for the movie to be saved at.
    file_name: Name of the movie file.
    fps: Frames Per Seconds
    figax: Figure, Axis object of an existing pitch.Default is None.
    field_dimensions:  Field dimensions in meters (Width x Height). Default is (106,68).
    home_team_color: Color of Home Team Players
    away_team_color: Color of Away Team Players
    marker: marker for the Players. Default is 'o'.
    include_plaer_velocities: Shows velocities of players. Default is False.
    player_alpha: Alpha. Default is 0.7
    
    
    """

    # Check if the indices are exactly the same for home and away team.
    assert np.all(list(tracking_home.index)==list(tracking_away.index)),"Tracking Home index should be same with Tracking Away index."

    if figax==None: #create new pitch
        fig,ax=plot_pitch(field_dimensions=field_dimensions)
    else: # overlay on existing pitch
        fig,ax=figax
    fig.set_tight_layout(True)
    
    # Either away or home team index
    index=tracking_away.index
    
    # Set Movie Settings
    metadata=dict(title="Tracking Data",comment="Metrica tracking data movie")
    ffmpeg=animation.FFMpegWriter(fps=fps,metadata=metadata)
    
    
    file_path=os.path.join(file_path,file_name+".mp4")
    
    # Generating movie process
    print("Generating movie..\nWait...")
    
    with ffmpeg.saving(fig=fig,outfile=file_path,dpi=100):
        
        # Get objects to be plotted per row
        # Plot one row, then delete axis objects and get objects from next row.
        for idx in index:
            objects=[]
            for team, color in zip([tracking_home.loc[idx],tracking_away.loc[idx]], [home_team_color,away_team_color]):
                    
                player_x_columns=[x for x in team.index if (re.match(r"Home_[0-9]+_x|Away_[0-9]+_x",x))]
                player_y_columns=[y for y in team.index if (re.match(r"Home_[0-9]+_y|Away_[0-9]+_y",y))]
                # Players' positions
                obj,=ax.plot(team[player_x_columns],team[player_y_columns],marker,color=color,markersize=10,alpha=player_alpha)
                objects.append(obj)
                if include_player_velocities:
                    vx_columns=[x.replace("_x","_vx") for x in player_x_columns]
                    vy_columns=[y.replace("_y","_vy") for y in player_y_columns]
                    obj=ax.quiver(team[player_x_columns],team[player_y_columns],team[vx_columns],team[vy_columns],color=color,alpha=1,
                                  scale_units='inches', scale=10.,width=0.0015,headlength=5,headwidth=3,zorder=4)
                    objects.append(obj)
            # Plot ball position
            obj,=ax.plot(team["ball_x"],team["ball_y"],marker,markersize=3,color='white')
            objects.append(obj)
            # Timer on top of the field
            frame_minute=int(team["Time [s]"]/60.0)
            frame_second=(team["Time [s]"]/60.0 - frame_minute)*60
            timer_text="{}:{:.1f}".format(frame_minute,frame_second) # Timer like '2:40'
            obj=ax.text(-8,field_dimensions[1]/2 +8,timer_text,bbox=dict(facecolor='#3C83F6', alpha=0.5,edgecolor='blue'))
            objects.append(obj)
            ffmpeg.grab_frame() #Grab the image information from the figure and save as a movie frame.
            # Delete all axis objects to create the next frame
            for object in objects:
                object.remove()
            
        print("Ready")
        plt.clf()
        plt.close(fig)
        
        

def plot_ball_position_at_goals(event,tracking_home,tracking_away):
    '''
    Plots ball position at goals of Home and Away Team.
    Note, that ball position is measured as the bosition at the END FRAME of the event.
    
    Parameters
    ----------
    event: pd.DataFrame containing events.
    tracking_home: pd.DataFrame with Tracking Data for Home team.
    tracking_away: pd.DataFrame with Tracking Data for Away team.
    Returns
    -------
    fig,ax1,ax2 : Figure , Axis objects of the  plot.
    
    '''
    
    # Goals
    goals=event.loc[~(event["Subtype"].isna()) & (event["Subtype"].str.contains("-GOAL"))]
    home_goal_indices=goals.loc[goals["Team"]=="Home","End Frame"]
    away_goal_indices=goals.loc[goals["Team"]=="Away","End Frame"]
    
    home_ball_xy,away_ball_xy=[],[]
    
    for ind in home_goal_indices:
        # Checking for Nan in case ball position was lost
        if np.isnan(tracking_home.loc[ind,"ball_x"]):
            home_ball_xy.append(tracking_home.loc[ind-3,["ball_x","ball_y"]].values)
        else:
            home_ball_xy.append(tracking_home.loc[ind,["ball_x","ball_y"]].values)
        
    for ind in away_goal_indices:
        # Checking for Nan in case ball position was lost
        if np.isnan(tracking_away.loc[ind,"ball_x"]): 
            away_ball_xy.append(tracking_away.loc[ind-2,["ball_x","ball_y"]].values)
        else:
            away_ball_xy.append(tracking_away.loc[ind,["ball_x","ball_y"]].values)
            
    # Lists and in Same direction
    away_ball_x=np.array([abs(53-abs(i[0])) for i in away_ball_xy])
    away_ball_y=np.array([abs(i[1]) for i in away_ball_xy])
    home_ball_x=np.array([abs(53-abs(i[0])) for i in home_ball_xy])
    home_ball_y=np.array([abs(i[1]) for i in home_ball_xy])
            
    #loading Ball Image
    BALL_PATH=os.path.join(os.getcwd(),"images","ball.png")
    ball_img=OffsetImage(plt.imread(BALL_PATH), zoom=0.06)
    
    
    fig, (ax1,ax2) =plt.subplots(2,1,figsize=(10,8),facecolor='silver')
    #Setting plot titles
    ax1.set_title("Away Goals' ball position")
    ax2.set_title("Home Goals' ball position")
    
    # Based on Pitch dimensions found on the Internet in yards.
    meters_per_yard=0.9144
    goal_height=3*meters_per_yard
    goal_line_width = 8*meters_per_yard
    # Setting ticks
    ax1.set_xticks(np.arange(-5,goal_line_width+5,1))
    ax2.set_xticks(np.arange(-5,goal_line_width+5,1))
    plt.yticks(np.arange(-5,goal_height+5,1))
    
    # Artists cannot be reused, so need to duplicate for every subplot.
    # Drawing goal with 2 vertical and one horizontal line.
    left_goalpost=plt.Line2D(np.array([0,0]),np.array([0,goal_height]),color='b',linewidth=1)
    right_goalpost=plt.Line2D(np.array([goal_line_width,goal_line_width]),np.array([0,goal_height]),color='b',linewidth=1)
    crossbar=plt.Line2D(np.array([0,goal_line_width]),np.array([goal_height,goal_height]),color='b',linewidth=1)
    left_goalpost1=plt.Line2D(np.array([0,0]),np.array([0,goal_height]),color='b',linewidth=1)
    right_goalpost1=plt.Line2D(np.array([goal_line_width,goal_line_width]),np.array([0,goal_height]),color='b',linewidth=1)
    crossbar1=plt.Line2D(np.array([0,goal_line_width]),np.array([goal_height,goal_height]),color='b',linewidth=1)
    for line in [left_goalpost,right_goalpost,crossbar]:
        ax1.add_line(line)
    for line in [left_goalpost1,right_goalpost1,crossbar1]:
        ax2.add_line(line)
        
    # transparent points
    ax1.scatter(away_ball_x,away_ball_y,alpha=0)
    ax2.scatter(home_ball_x,home_ball_y,alpha=0)
    
    # Adding Ball Image on top of scatter points for each team
    for x,y in zip(away_ball_x,away_ball_y):
        ab1=AnnotationBbox(ball_img,(x,y),frameon=False)
        ax1.add_artist(ab1)
        
    for x,y in zip(home_ball_x,home_ball_y):
        ab2=AnnotationBbox(ball_img,(x,y),frameon=False)
        ax2.add_artist(ab2)    
    
    
    plt.tight_layout()
    ax1.axis('off')
    ax2.axis('off')
    
    return fig,ax1,ax2


def plot_pitch_control_for_event(event_id,event,tracking_home,tracking_away,pc_att,x_grid,y_grid,annotate_player=False,field_dimensions = (106.0,68.0),include_player_velocities=False,alpha=0.6):
    '''
    Plot Pitch control for a single event.
    By default gray indicates area in which Home Team Players have control, whereas for red Away Team Players.
    
    Parameters
    ----------
    event_id: int , should be a valid id
    event: pd.Dataframe with Event Data.
    tracking_home: pd.Dataframe with Tracking Data for Home Team.
    tracking_away: pd.Dataframe with Tracking Data for Away Team.
    pc_att: np.array with Pitch Control of Attacking Team, i.e. probability to get the ball at certain locations.
    x_grid: np.array with positions of grid cells in x-axis
    y_grid: np.array with positions of grid cells in y-axis
    annotate_player: Annotate Player. Default is False.
    field_dimensions:  Field dimensions in meters (Width x Height). Default is (106,68).
    include_player_velocities: Shows velocities of players. Default is False.
    alpha: Alpha of colors for pitch control. Default is 0.6
    
    Returns
    -------
    fig,ax: Figure and axis Objects of Pitch with pitch control for an event.
    '''
    
    frame=event.loc[event_id,"Start Frame"]
    team_in_possession=event.loc[event_id,"Team"]
    
    if team_in_possession=="Away":
        colors=["black","white","red"] #0-->1
    else: # Home in possession
        colors=["red","white","black"] #0-->1
    
    fig,ax=plot_pitch(field_dimensions,field_color="white")
    plot_frame(tracking_home.loc[frame],tracking_away.loc[frame],include_player_velocities,field_dimensions,player_alpha=0.9,figax=(fig,ax),
               annotate_player=annotate_player,ball_color='green',markersize=8.2)
    plot_events(event.loc[event_id:event_id],figax=(fig,ax),color=colors[2])
    

    cmap=matplotlib.colors.LinearSegmentedColormap.from_list('pc_colors',colors) # Needs Default number of bins(256)!!
    
    
    # interpolation: the one that works better
    # vmin,vmax=(0,1) because probability values for pitch control are between range(0,1)
    # need to flip to get start upper left
    ax.imshow(np.flipud(pc_att),extent=(-field_dimensions[0]/2,field_dimensions[0]/2,-field_dimensions[1]/2,field_dimensions[1]/2),origin="upper", # Upper left is [0,0]
              interpolation="lanczos",cmap=cmap,vmin=0,vmax=1,alpha=alpha)
    
    
    return fig,ax
    

def plot_EPV_grid(epv_grid,attacking_direction,field_dimensions=(106.0,68.0)):
    '''
    Plots EPV grid.
    
    Parameters
    ----------
    epv_grid: Preloaded epv_grid. Default 32x50
    attacking_direction: 1 if left to right (Home Team), -1 if right to left (Away Team)
    field_dimensions:  Field dimensions in meters (Width x Height). Default is (106,68).
    
    '''
    
    if attacking_direction==1: # Home team
        cmap='Greys'
    elif attacking_direction==-1: # Away team
        cmap='Reds'
        epv_grid=np.fliplr(epv_grid) # reverse direction
    else:
        raise Exception("Invalid team name.")
    
    
    fig,ax=plot_pitch(field_dimensions,field_color="white",alpha=0.2)
    
    # None interpolation looks like squares
    ax.imshow(epv_grid,extent=(-field_dimensions[0]/2,field_dimensions[0]/2,-field_dimensions[1]/2,field_dimensions[1]/2), # Upper left is [0,0]
              cmap=cmap,norm=matplotlib.colors.Normalize(vmin=0,vmax=0.6))


def plot_EPV_grid_for_event(event_id,event,tracking_home,tracking_away,epv_grid,pc_att,annotate_player=False,field_dimensions = (106.0,68.0),include_player_velocities=False,alpha=0.6,contour=False):
    
    '''
    Plots Expected value of EPV at given event_id. (EPV*PPCF)
    
    Parameters
    ----------
    event_id: int , should be a valid id
    event: pd.Dataframe with Event Data.
    tracking_home: pd.Dataframe with Tracking Data for Home Team.
    tracking_away: pd.Dataframe with Tracking Data for Away Team.
    epv_grid: Preloaded epv_grid. Default 32x50
    pc_att: np.array with Pitch Control of Attacking Team, i.e. probability to get the ball at certain locations.
    annotate_player: Annotate Player. Default is False.
    field_dimensions:  Field dimensions in meters (Width x Height). Default is (106,68).
    include_player_velocities: Shows velocities of players. Default is False.
    alpha: Alpha of colors for pitch control. Default is 0.6
    contour: Add contours to areas with Expected EPV > 75% of max(expected EPV). Default is False
    Returns
    -------
    fig,ax:Figure and axis Objects of Expected EPV for an event.
    
    '''
    
    pass_frame=event.loc[event_id,"Start Frame"]
    team_in_possession=event.loc[event_id,"Team"]
    
    attacking_direction=mio.find_attacking_direction(team_in_possession)
    if attacking_direction==1: # Home team
        cmap='Greys'
    else: # Away team
        cmap='Reds'
        epv_grid=np.fliplr(epv_grid) # reverse direction
    
    #plot pitch, event and frame
    fig,ax=plot_pitch(field_color="white",field_dimensions=field_dimensions)
    plot_frame(tracking_home.loc[pass_frame],tracking_away.loc[pass_frame],field_dimensions=field_dimensions,figax=(fig,ax),include_player_velocities=include_player_velocities,
               player_alpha=alpha,annotate_player=annotate_player,ball_color='green',markersize=8.2)
    plot_events(event.loc[event_id:event_id],figax=(fig,ax),color='green',alpha=1)
    

    
    # EPV * PPCF
    epvXppcf=pc_att*epv_grid
    
    vmax=np.max(epvXppcf)*1.5 # not too dark
    ax.imshow(np.flipud(epvXppcf), extent=(-field_dimensions[0]/2., field_dimensions[0]/2., -field_dimensions[1]/2., field_dimensions[1]/2.),
              interpolation='lanczos',vmin=0.0,vmax=vmax,cmap=cmap,alpha=0.9)
    

    # Add contour to areas within 75% of max epv*ppcf
    if contour:
        # can add multiple contours if there are multiple such areas
        ax.contour(epvXppcf,extent=(-field_dimensions[0]/2., field_dimensions[0]/2., -field_dimensions[1]/2., field_dimensions[1]/2.),levels=np.array([0.75])*np.max(epvXppcf),
               vmin=0.0,vmax=vmax,colors='blue')
    
    return fig,ax

    
    
    
    
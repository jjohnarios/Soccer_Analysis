# -*- coding: utf-8 -*-
"""

Simplified Pitch Control Model.
Key Assumptions (from William Spearman):
    Ball has steady speed of 15 m/s that is Ball_Arival_Time= (End_pos-Start_pos)/15
    Player has steady speed of 5 m/s. When going towards ball they move with 5 m/s
    Initial reaction time of a Player is 0.7 seconds. During this time the player continues moving along their current trajectory.
    After 0.7 seconds the player starts moving towards the ball location at the speed of 5m/s
    Control Probability of Player = λ * Dt 
        Dt: Time interval near the ball
        λ: 4.3 inverse seconds that is it takes 1/4.3~=0.235 seconds for a Player to control the ball
    
    Standard Deviation by the cumulative distribution function of the Logistic Function is 0.45 (σ=0.45).
    

Inspiration by: Friends-of-Tracking-Data-LaurieOnTracking

@author: Apatsidis Ioannis
"""
import numpy as np


def get_model_parameters():
    '''
    Setting some parameters for the simplefied model based on the asssumptions made.
    
    Returns
    -------
    params: Dictionary with model parameters
    '''
    params={}
    params["ball_speed"]=15 # 15 m/s steady velocity
    params["player_speed"]=5 # 5 m/s steady velocity
    params["reaction_time"]=0.7 # 0.7 m/s initial reaction time
    params["lambda"]=4.3 # 4.3 inverse seconds -> How fast can a player control the ball , Prob= lambda * Dt , Dt: time near the ball
    params["lambda_gk"]=4.3 * 3 # Goalkeeper has advantage of being able to catch the ball
    params["sigma"]=0.45 # 0.45 seconds , standard deviation of sigmoid to add uncertainty of player arrival time
    
    # If a player arrives at target location control_time seconds before the next Player then the first one has enough time to control the
    # ball so we don't need to calculate pitch control explicitly.
    params["control_time"]=np.sqrt(3)*params["sigma"]/np.pi+1/params["lambda"] # seconds to control the ball , assuming same for def and att.
    
    # numerical parameters for model evaluation
    params['int_step'] = 0.04 # integration timestep seconds dT
    params['max_int_time'] = 10 # upper limit on integral time seconds
    params['model_converge_tol'] = 0.01 # assume convergence when pitch control>0.99 at a given location.

    
    return params

def init_players(team_tracking,team_name,params,GK_NAME):
    '''
    Initialises Player Objects for current frame
    
    Parameters
    ----------
    team_tracking: pd.Series with Tracking Data for a single Frame
    team_name: name of Team like "Home", "Away"
    params: dictionary with model parameters
    GK_NAME: name of Goalkeeper like "Home_11" or "Away_25"
    
    Returns
    -------
    players_list: List with Player Objects in current Frame
    '''
    
    # Get all players , e.g. Home_1 , Away_2
    players=np.unique(([x.split('_')[0]+'_'+x.split('_')[1] for x in team_tracking.index if team_name in x]))
    
    players_list=[]
    # Create Player object and add that to the returned list if Player is in currecnt frame
    for p in players:
        player=Player(p,team_tracking,params,GK_NAME)
        if player.inframe:
            players_list.append(player)
    
    return players_list
    

def check_offsides(attacking_team,attacking_players,defending_players,ball_start_pos,field_dimensions=(106.,68.),tol=0.2):
    '''
    Checks if any attacking player is offside in the current Frame.
    A player is offside if:
        They are in front of their own half of the field and the ball.
        They are in front of the second last defender.
    Doesn't take into consideration passive offside, that is players who are not involved.
    
    Parameters
    ----------
    attacking_team: Attacking team like "Home" or "Away"
    attacking_players: list of Player Objects of the attacking team
    defending_players: list of Player Objects of the defending team
    ball_start_pos: tuple with (x,y) coordinates of the ball in the current Frame
    field_dimensions: Field dimensions in meters (Width x Height). Default is (106,68).
    tol: Tolerance for Offside in meters. Default value is 0.2 meters.
    
    Returns
    -------
    non_offside_attacking_players: List with all the attacking players who are not offside.
    '''
    
    ball_x=ball_start_pos[0]
    non_offside_attacking_players=[]
    
    x_def_positions=[player.position[0] for player in defending_players] # x coordinates of Defending players
    
    if attacking_team=="Home": # direction of attack --->
        second_last_def_x_pos=sorted(x_def_positions,reverse=True)[1]+tol  # x position of second last defender + tol meters
        
        for player in attacking_players:
            if player.position[0]<=ball_x or player.position[0]<=0: # Not Offside, behind the ball or behind center line
                non_offside_attacking_players.append(player)
            elif  player.position[0] <= second_last_def_x_pos: # Not Offside
                non_offside_attacking_players.append(player)
            else:
                print("Player {} is OFFSIDE!".format(player.name))
    else: # Away , direction of attack <----
        second_last_def_x_pos=sorted(x_def_positions)[1]  -tol # x position of second last defender + tol meters
        
        for player in attacking_players:
            if player.position[0]>=ball_x or player.position[0]>=0:# Not Offside, behind the ball or behind center line
                non_offside_attacking_players.append(player)
            elif player.position[0] >= second_last_def_x_pos: # Not Offside
                non_offside_attacking_players.append(player)
            else:
                print("Player {} is OFFSIDE!".format(player.name))
                
                
    return non_offside_attacking_players
        
        




class Player():
    '''
    This class represents a Player. It is used mainly for pitch control.
    
    '''
    
    def __init__(self,name,team_tracking,params,GK_NAME):
        '''
        Initializes name, team name , reaction time , position , player speed, sigma (σ), lambda (λ) and velocities
        
        Parameters
        ----------
        name: Player Name like "Home_23" or "Away_4"
        team_tracking: pd.Series with Tracking Data for a single Frame
        params: Model Parameters
        GK_NAME: Goalkeeper name like "Home_3" or "Away_15"
                
        '''
        
        self.name=name # Name like "Away_12"
        self.teamname=name.split("_")[0] # Team name like "Team" or "Home"
        self.reaction_time=params["reaction_time"] # Reaction Time 0.7 seconds
        self.position=np.array([team_tracking.loc[self.name+"_x"],team_tracking.loc[self.name+"_y"]]) # (x,y) position
        self.inframe= not np.any(np.isnan(self.position)) # Checks if player is in current frame or bench player
        self.max_vel=params["player_speed"] # Maximum player velocity 15m/s.
        self.sigma=params["sigma"] # Uncertainty to time_to_intercept
        self.lambda_param=params["lambda_gk"] if self.name==GK_NAME else params["lambda"] # 1/λ is time to control ball      
        
        self.__set_velocity(team_tracking) # Sets player velocities
        
        self.PPCF=0 # Potential Pitch Control Field


    
    def __set_velocity(self,team_tracking):
        '''
        Set velocity of Player. If vel is nan then sets velocity to (0,0).
        
        Parameters
        ----------
        team_tracking: pd.Series with Tracking Data for a single Frame
        '''
        self.velocity=np.array([team_tracking.loc[self.name+"_vx"],team_tracking.loc[self.name+"_vy"]])
        
        if np.any(np.isnan(self.velocity)):
            self.velocity=np.array([0,0])
        
    def get_time_to_intercept(self,target_pos):
        '''
        Calculates time to intercept to target_pos position. First calculates position for the reaction time interval and then
        adds that to the actual time to intercept during which the player is moving towards the ball.
         
        Parameters
        ----------
        target_pos: Target position to intercept( position of the ball).
        
        Returns
        -------
        ttt: Time to intercept
        
        '''
        self.PPCF=0
        
        reaction_pos=self.position+ self.velocity*self.reaction_time
        dx=np.sqrt((target_pos[0]-reaction_pos[0])**2 + (target_pos[1]-reaction_pos[1])**2) # Euclidean Distance
        # After reaction time , player moves with steady velocity = maxvel.
        tti= self.reaction_time+ dx/self.max_vel
        
        return tti
        
        
        
    def get_probability_to_intercept(self,T,target_pos):
        '''
        Calculates the probability for a Player to intercept the ball at T time.
        P_int(T)=1/(1+ e^(-(T-t_int)/(√3 σ/π)) )
        
        Parameters
        ----------
        T: time in seconds
        target_pos: Target position to intercept( position of the ball).
        
        Returns
        -------
        prob: Probability to intercept.

        '''
        
        time_to_intercept=self.get_probability_to_intercept(target_pos)
        
        prob=self.reaction_time+ 1/(1+np.exp(- (T - time_to_intercept)/((np.sqrt(3)*self.sigma)/np.pi)))
        return prob
    
    
    def __str__(self):
        '''
        String represantation of a Player.
        '''
        
        p_str=("Name: {0}\nTeam: {1}\nReaction Time: {2} seconds\nPosition(x,y): {3}\nSpeed(Max-steady): {4} m/s\n"
              "Current Velocity(vx,vy): {5}\nSigma: {6}\nLambda: {7}").format(self.name,
                          self.teamname,self.reaction_time,self.position,
                          self.max_vel,self.velocity,self.sigma,self.lambda_param)
        return p_str
    
    
    
    
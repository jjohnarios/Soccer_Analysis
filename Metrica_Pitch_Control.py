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
    params["ball_speed"]=15. # 15 m/s steady velocity
    params["player_speed"]=5. # 5 m/s steady velocity
    params["reaction_time"]=0.7 # 0.7 m/s initial reaction time
    # 4.3 inverse seconds -> How fast can a player control the ball , Prob= lambda * Dt , Dt: time near the ball
    params["lambda_att"]=4.3 # attack
    params["lambda_def"]=4.3 # defence (If multiplied by 1.72 based on Spearman , defenders have an advantage)
    params["lambda_gk"]=4.3 * 3 # Goalkeeper has advantage of being able to catch the ball
    params["sigma"]=0.45 # 0.45 seconds , standard deviation of sigmoid to add uncertainty of player arrival time
    
    # If a player arrives at target location control_time seconds before the next Player then the first one has enough time to control the
    # ball so we don't need to calculate pitch control explicitly.
    params["control_time"]=3*np.log(10) * (np.sqrt(3)*params['sigma']/np.pi + 1/params['lambda_att']) # seconds to control the ball , assuming same for def and att.
    
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
        if player.inframe: # In current frame
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
    
    ball_x=ball_start_pos[0] # Start X
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
        
        


def find_pitch_control_for_event(event_id,event,tracking_home,tracking_away,params,GK_NAMES,field_dimensions=(106.,68.),num_grid_cells_x=53,offsides=True):
    
    '''
    Calculates pitch control for an event for the entire field.
    Field is divided to a grid.
    
    Parameters
    ----------
    event_id: int , should be a valid id
    event: pd.Dataframe with Event Data.
    tracking_home: pd.Dataframe with Tracking Data for Home Team.
    tracking_away: pd.Dataframe with Tracking Data for Away Team.
    params: dictionary with model parameters
    GK_NAMES: tuple with goalkeeper names like (GK_Home_Team,GK_Away_Team)
    field_dimensions: Field dimensions in meters (Width x Height). Default is (106,68).
    num_grid_cells_x:Number of grid cells in x-axis to divide field_dimensions[0] to. Default is 53.
    offsides: Take into consideration players who are offside , that is do not calculate their pitch control. Default value is True.
    
    Returns
    -------
    pc_grid_att: Pitch control grid containing pitch control probability for the attacking team.
                 For defending team pc_grid_def= 1 - pc_grid_att
    x_grid: Positions of centers of cells in x-axis (field length).
    y_grid: Positions of centers of cells in y-axis (field width).
    
    '''
    
    # Check if the indices are exactly the same for home and away team.
    assert np.all(list(tracking_home.index)==list(tracking_away.index)),"Tracking Home index should be same with Tracking Away index."
    
    pass_frame=event.loc[event_id,"Start Frame"]
    team_with_possession=event.loc[event_id,"Team"]
    ball_start_pos=event.loc[event_id,["Start X","Start Y"]]
    ball_start_pos=np.array(ball_start_pos,dtype='float')
    
    num_grid_cells_y= int(field_dimensions[1]/(field_dimensions[0]/num_grid_cells_x))
    grid_dimensions=(field_dimensions[0]/num_grid_cells_x,field_dimensions[1]/num_grid_cells_y) # Default 2x2 meters    
    x_grid,y_grid=[],[]
    
    # Position of a cell of the grid is the xy coordinates of its center
    # -  -  -
    # -  @  -
    # -  -  -
    
    # Calculating x positions
    for i in range(num_grid_cells_x):
        x_grid.append(-field_dimensions[0]/2 + (i*2+1)* (grid_dimensions[0]/2))
    # Calculating y positions
    for i in range(num_grid_cells_y):
        y_grid.append(field_dimensions[1]/2 - (i*2+1)*(grid_dimensions[1]/2))
    x_grid=np.array(x_grid)
    y_grid=np.array(y_grid)*np.array([-1])
    # Pitch Control Grids for Attacking and Defending team    
    # In shape (y,x) not (x,y)
    pc_grid_att=np.zeros((num_grid_cells_y,num_grid_cells_x))
    pc_grid_def=np.zeros((num_grid_cells_y,num_grid_cells_x))

    # Initialise Players positions , velocities etc. for Home and Away Team
    if team_with_possession=="Home":
        attacking_players=init_players(tracking_home.loc[pass_frame],"Home",params,GK_NAMES[0])
        defending_players=init_players(tracking_away.loc[pass_frame],"Away",params,GK_NAMES[1])
    else: # Away
        defending_players=init_players(tracking_home.loc[pass_frame],"Home",params,GK_NAMES[0])
        attacking_players=init_players(tracking_away.loc[pass_frame],"Away",params,GK_NAMES[1])        
        
    # Do not calculate attacking players pitch control if they are offside    
    if offsides:
        attacking_players=check_offsides(team_with_possession,attacking_players,defending_players,ball_start_pos,field_dimensions) 
    # For every cell calculate pitch control
    for i in range(len(y_grid)):
        for j in range(len(x_grid)):
            target_pos=np.array([x_grid[j],y_grid[i]])
            pc_grid_att[i,j],pc_grid_def[i,j]=pitch_control_at_pos(target_pos,attacking_players,defending_players,ball_start_pos,params)
            #pc_grid_att[i,j],pc_grid_def[i,j]=calculate_pitch_control_at_target(target_pos,attacking_players,defending_players,ball_start_pos,params)
            #print(pc_grid_att[i,j],pc_grid_def[i,j])
    #check probability sums within convergence
    checksum=np.sum(pc_grid_att+pc_grid_def)/float(num_grid_cells_x*num_grid_cells_y)
    assert 1-checksum< params["model_converge_tol"],"Checksum failed: {1.3f}".format(1-checksum)
    
    return pc_grid_att,x_grid,y_grid
    

def pitch_control_at_pos(target_pos,attacking_players,defending_players,ball_start_pos,params):
    
    '''
    Calculates Total Pitch Control of the attacking and defending team for a given ball position.
    It is based on Spearman's Equation 6  at Physics-Based Modeling of Pass Probabilities in Soccer.
    
    Parameters
    ----------
    target_pos: np.array with (x,y) cordinates of the the target pos (i.e. center of a cell of the grid)
    attacking_players: list of Player Objects of the attacking team
    defending_players: list of Player Objects of the defending team
    ball_start_pos:  tuple with (x,y) coordinates of the ball in the current Frame
    params: dictionary with model parameters
    
    Returns
    -------
    pc_att[i-1]: np.array with total attacking players pitch control probability at the target pos (cell of grid).
    pc_def[i-1]: np.array with total attacking players pitch control probability at the target pos (cell of grid).
    
    '''
    
    # Player with cell control means lowest value of "Time to intercept + Time to control"
    
    # Find ball_flight_time
    if np.any(np.isnan(ball_start_pos)):
        ball_flight_time=0.
    else:
        ball_flight_time=np.sqrt((target_pos[0]-ball_start_pos[0])**2 + (target_pos[1]-ball_start_pos[1])**2) / params["ball_speed"]
    # Min arrival time of attacking and defending players
    min_at_att=np.nanmin([player.get_time_to_intercept(target_pos) for player in attacking_players])
    min_at_def=np.nanmin([player.get_time_to_intercept(target_pos) for player in defending_players])
    

    
    if (min_at_att-max(min_at_def,ball_flight_time)>=params["control_time"]):
        # Defender has enough time to control the ball, before attacker arrives so no need to calculate pitch control
        return 0,1
    elif (min_at_def-max(min_at_att,ball_flight_time)>=params["control_time"]):
        # Attacker has enough time to control the ball, before defender arrives so no need to calculate pitch control
        return 1,0
    else: # calculate pitch control
        # keep ONLY players who are not far from target location (need time to reach target < control_time of the one reached already)
        defending_players=[player for player in defending_players if player.time_to_intercept-min_at_def < params["control_time"]]
        attacking_players=[player for player in attacking_players if player.time_to_intercept-min_at_att < params["control_time"]]
        

        # integration (int_step elements)
        dt_array=np.arange(ball_flight_time-params['int_step'],ball_flight_time+params['max_int_time'],params['int_step'])
        pc_att=np.zeros_like(dt_array) # Pitch Control Attacking Team
        pc_def=np.zeros_like(dt_array) # Pitch Control Defending Team
        
        # Integrate Spearman's Equation until Convergence or exceeds array size, time limit (Eq. 6 at Physics-Based Modeling of Pass Probabilities in Soccer)
        total_pc_prob=0.0
        i=1
        while 1-total_pc_prob>params['model_converge_tol'] and i<dt_array.size:
            
            T=dt_array[i] # Time T within a player can reach target pos
            for player in attacking_players:
                # calculate ball control probability for player in time interval T+int_step
                
                pc_dT= (1-pc_att[i-1]-pc_def[i-1])*player.get_probability_to_intercept(T)*player.lambda_att
                assert pc_dT>=0," Invalid attacking player probability"
                player.PPCF+= pc_dT*params["int_step"] # contribution of this player to pitch control
                # summing all players contribution = total pitch control for attacking team

                pc_att[i]+=player.PPCF
            for player in defending_players:
                # calculate ball control probability for player in time interval T+int_step
                pc_dT= (1-pc_att[i-1]-pc_def[i-1])*player.get_probability_to_intercept(T)*player.lambda_def
                assert pc_dT>=0," Invalid defending player probability"
                player.PPCF+= pc_dT*params["int_step"] # contribution of this player to pitch control
                # summing all players contribution = total pitch control for attacking team
                pc_def[i]+=player.PPCF
            total_pc_prob=pc_def[i]+pc_att[i] # We need >0.99
            i+=1
        
        if i>=dt_array.size:
            print("Integration couldn't converge. Total Pitch Control Probability: ",total_pc_prob)
        
        print(pc_att[i-1])
        print(pc_def[i-1])
        return pc_att[i-1],pc_def[i-1]



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
        self.lambda_att=params["lambda_att"]
        self.lambda_def=params["lambda_gk"] if self.name==GK_NAME else params["lambda_def"] # 1/λ is time to control ball      
        
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
        self.PPCF=0 # resetting to zero
        
        reaction_pos=self.position+ self.velocity*self.reaction_time
        dx=np.sqrt((target_pos[0]-reaction_pos[0])**2 + (target_pos[1]-reaction_pos[1])**2) # Euclidean Distance
        # After reaction time , player moves with steady velocity = maxvel.
        tti= self.reaction_time+ dx/self.max_vel
        self.time_to_intercept=tti # I need this for get_probability_to_intercept
        
        return tti
        
        
        
    def get_probability_to_intercept(self,T):
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
        prob = 1/(1. + np.exp( -np.pi/np.sqrt(3.0)/self.sigma * (T-self.time_to_intercept) ) )
        return prob
    
    
    def __str__(self):
        '''
        String represantation of a Player.
        '''
        
        p_str=("Name: {0}\nTeam: {1}\nReaction Time: {2} seconds\nPosition(x,y): {3}\nSpeed(Max-steady): {4} m/s\n"
              "Current Velocity(vx,vy): {5}\nSigma: {6}\nLambda Att: {7}\nLambda Def: {8}\nPPCF: {9}").format(self.name,
                          self.teamname,self.reaction_time,self.position,
                          self.max_vel,self.velocity,self.sigma,self.lambda_att,self.lambda_def,self.PPCF)
        return p_str
    
    
    
    
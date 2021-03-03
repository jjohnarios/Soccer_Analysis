# -*- coding: utf-8 -*-
"""


Inspiration by: Friends-of-Tracking-Data-LaurieOnTracking

@author: Apatsidis Ioannis
"""

import numpy as np
import Metrica_Pitch_Control as mpc

def load_EPV_grid(file_name="EPV_grid.csv"):
    '''
    Loads a predefined EPV grid from @LauriOnTracking into a numpy array.
    Default shape is 32x50 and default direction is left to right.
    
    Parameters
    ----------
    file_name: name of file containing the epv grid
    
    Returns
    -------
    epv_grid: Grid with Expected possession values at each cell of the grid.
    
    '''
    
    epv_grid=np.genfromtxt("EPV_grid.csv",delimiter=',')
    
    return epv_grid

def __get_EPV_at_location(start_pos,epv_grid,team_with_possession,field_dimensions=(106.,68.)):
    
    '''
    Get EPV at given location.
    
    Parameters
    ----------
    start_pos: (x,y) of location in pitch
    epv_grid: Grid with Expected possession values at each cell of the grid.
    field_dimensions:  Field dimensions in meters (Width x Height). Default is (106,68).
    team_with_possession: Attacking team. "Home" or "Away".
    
    Returns
    -------
    epv_grid[y_ind,x_ind] : EPV at given position
    '''
    
    # Flip EPV grid if Away Team is attacking
    if team_with_possession=="Away":
        epv_grid=np.fliplr(epv_grid)
    
    # Intuitively think x and y as they are at the pitch
    
    # x,y coordinates of start_pos
    x,y=start_pos[0],start_pos[1]
    # lenx,leny of epv_grid
    lenx_epv_grid,leny_epv_grid=epv_grid.shape[1],epv_grid.shape[0]
    
    # len of sides of cells of grid
    cell_x=field_dimensions[0]/lenx_epv_grid
    cell_y=field_dimensions[1]/leny_epv_grid
    
    x_ranges=np.linspace(-((lenx_epv_grid/2) *cell_x),(lenx_epv_grid/2) *cell_x,lenx_epv_grid)
    y_ranges=np.linspace((leny_epv_grid/2) *cell_y, -((leny_epv_grid/2) *cell_y) ,leny_epv_grid)
    
    # Indices in epv_grid
    x_ind,y_ind=100,100
    
    for i in range(1,len(x_ranges)):
        if x<=x_ranges[i]:
            x_ind=i-1
            break
    # Edge case
    if x==x_ranges[-1]:
        x_ind=len(x_ranges)-1 
    
    for j in range(1,len(y_ranges)):
        if y>=y_ranges[j]:
            y_ind=j-1
            break
    # Edge case
    if y==y_ranges[-1]:
        y_ind=len(y_ranges)-1 
        

    return epv_grid[y_ind,x_ind]
    



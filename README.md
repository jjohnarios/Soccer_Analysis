 # Soccer Data Analysis  :soccer:
 
Working with Metrica's tracking and event data for Soccer Analytics. Providing insightful pitch visualizations and clips from soccer matches.
Pitch Control to find controlled regions from teams is provided and EPV to calculate the probability that a possession leads to a goal.
 
![Python](https://img.shields.io/badge/-Python-yellow) ![Jupyter Notebook](https://img.shields.io/badge/-JupyterNotebook-cyan)

## About the data
- Two Sample Games in standar CSV format with synchronized Tracking and Event data (Metrica Sports).
- Details and proper documentation of the data can be found in the link above.
- Source: https://github.com/metrica-sports/sample-data

## General
- Default Pitch dimensions are **106 x 68 meters**.
- Home Team Players by default are colored **black** :black_circle: and Away Team Players are colored **red** :red_circle:.
- White Dot represents the ball.
- Arrows represent player velocities. Longer arrows indicate running faster.
- Numbers indicate players jerseys numbers.

<p align="center">
  <img src="images/Pitch_ReadMe.png" width="600" title="Pitch Vizualization">
</p>

## Potential Pitch Control Field - PPCF
- How Teams control regions,pass probability for an imaginary ball placed at every point on the pitch.
- Pitch Control at a Target Location is the probability that a team or a player will be able to control the ball if it were at that location.
- Gray regions are controlled by Home Team (black color :black_circle:)
- Red regions are controlled by Away Team (red color :red_circle:)
- Green Dot represents the ball.
- Player 6 passes at an area controlled by his teammate Player 4. That indicates higher success pass probability.

<p align="center">
  <img src="images/Pitch_Control_Readme.png" width="600" title="Pitch Control for certain frame">
</p>

## Expected Possession Value - EPV
- EPV quantifies the value of possessing the ball at a given instance.
- It's the probability that the current possession will end in a goal given the current situation (ball & player position,match state etc.)
- Simplier approach: ![equation1](http://www.sciweavers.org/tex2img.php?eq=EPV%20%3D%20P_%7Bposs%7D%28G%20%5Cmid%20ball%2Cmatch%20state%29&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)
- Expected EPV at position pos: ![equation2](http://www.sciweavers.org/tex2img.php?eq=ExpectedEPV_%7Bpos%7D%20%3D%20EPV_%7Bpos%7D%20%2A%20PPCF_%7Bpos%7D&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)
- Expected EPV added of a pass from pos1 to pos2: ![equation3](http://www.sciweavers.org/tex2img.php?eq=EPVadded%3DExpectedEPV_%7Bpos2%7D%20-%20ExpectedEPV_%7Bpos1%7D&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)
- Contour areas below represent high EPV added options. Player 19 passes the ball and 0.012 EPV is added

<p align="center">
  <img src="images/Expected_EPV_at_821_and_PPCF.png" width="600" title="Expected EPV and PPCF.">
</p>

## Resources
For deep understanding of the formulas and the method used I suggest reading these amazing publications from William Spearman et al.:
- [Physics-Based Modeling of Pass Probabilities in Soccer](https://www.researchgate.net/publication/315166647_Physics-Based_Modeling_of_Pass_Probabilities_in_Soccer)
- [Beyond Expected Goals](https://www.researchgate.net/publication/327139841_Beyond_Expected_Goals)
- [EPV Calculation Approach](http://nessis.org/nessis11/rudd.pdf)

## Acknowledgments
- Thanks to "Friends of Tracking Data" for the useful content in soccer analytics.
- EPV_grid.csv from HarvardSoccer.


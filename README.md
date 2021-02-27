 # Soccer Data Analysis  :soccer:
 
Working with Metrica's tracking and event data for Soccer Analytics. Providing insightful pitch visualizations and clips from soccer matches.
Pitch Control to find controlled regions from teams is provided.
 
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

## Pitch Control
- How Teams control regions,pass probability for an imaginary ball placed at every point on the pitch.
- Pitch Control at a Target Location is the probability that a team or a player will be able to control the ball if it were at that location.
- Gray regions are controlled by Home Team (black color :black_circle:)
- Red regions are controlled by Away Team (red color :red_circle:)
- Green Dot represents the ball.
- Player 6 passes at an area controlled by his teammate Player 4. That indicates higher success pass probability.

<p align="center">
  <img src="images/Pitch_Control_Readme.png" width="600" title="Pitch Control for certain frame">
</p>


## Resources
For deep understanding of the formulas and the method used I suggest reading these amazing publications from William Spearman et al.:
- [Physics-Based Modeling of Pass Probabilities in Soccer](https://www.researchgate.net/publication/315166647_Physics-Based_Modeling_of_Pass_Probabilities_in_Soccer)
- [Beyond Expected Goals](https://www.researchgate.net/publication/327139841_Beyond_Expected_Goals)

## Acknowledgments
- Thanks to "Friends of Tracking Data" for the useful content in soccer analytics.


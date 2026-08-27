# Blackjack Strategy Simulator and Game

Two Python projects, one that lets the user play a game of blackjack, the other providing insights on a basic strategy decision table.

# Blackjack Strategy Simulator

The project models a player's decisions, hitting, standing, doubling, or splitting, all in accordance to a basic strategy lookup table. Variations on hand length and number of simulations are conducted, providing insight into the resulting profit and loss. 

## Rules of this game

- Two deck shoe
- Cut card is one deck deep
- DAS is allowed
- When aces are split, they hit and then stand, no resplitting or doubling allowed
- Resplits are allowed (apart from aces)

## Mathematical background

 The simulation uses a large number of random trials via having a new randomly shuffled shoe.

 By running a large number of these games, the model can estimate multiple different quantities including average profit, probability of winning, risk of bust. This is an example of Monte Carlo simulation.

 ## Results
 
 From runinng the project, here is a collection of results:

 ### Simulation of 100,000 hands of length 1000
 

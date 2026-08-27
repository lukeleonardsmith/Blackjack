# Blackjack Strategy Simulator and Game

Two Python projects, one that lets the user play a game of blackjack, the other providing insights on a basic strategy decision table.

# Blackjack Strategy Simulator

The project models a player's decisions, hitting, standing, doubling, or splitting, all in accordance to a basic strategy lookup table. Variations on hand length and number of simulations are conducted, providing insight into the resulting profit and loss. 

## Rules of this game

- Two deck shoe
- Cut card is one deck deep
- Dealer stands on 17
- DAS is allowed
- When aces are split, they hit and then stand, no resplitting or doubling allowed
- Resplits are allowed (apart from aces)
- Initial bankroll is 100
- Bet size is 1 (doubling and splitting result in 1 being added to the bet)
- Blackjack pays 3:2
- No surrender

## Mathematical background

 The simulation uses a large number of random trials via having a new randomly shuffled shoe.

 By running a large number of these games, the model can estimate multiple different quantities including average profit, probability of winning, risk of bust. This is an example of Monte Carlo simulation.

 ## Results
 
 From runinng the project, here is a collection of results:

 ### Simulation of 100,000 hands of length 1000
 
 ![Distribution of simulated profits](images/profit_distribution_100000_1000.png)

 After this simulation, the above histogram shows the profit attained after 1000 turns, and more detailed statistics are below (4sf):

 - Mean profit = -2.921
 - Median profit = -3.000
 - Standard deviation = 37.31
 - Best result = 151
 - Worst resilt = -100
 - Probability of profit = 0.4662
 - Probability of loss = 0.5284
 - Probability of bust = 0.004460

The same data has been gathered for Simulations of 1000 hands of 1000 turns and 1000 hands of 100 turns and are noted in the file named data. 

# Blackjack Game

This game is set up with the sme rules that governed the simulation, but the code itself is different due to allowing human input rather than being fully self contained.

## Features
- Start with a bankroll of 100 with a fixed betsize of 1
- Ability to hit, stand, double and split
- Can choose to see basic strategy recommendation

# Future Goals

I wish to also add a separate simulation with a Hi-Lo card counting system in place, with the option for choosing which variations to play, yet this would need far more research of my own into card counting. This could lead into comparisons of Hi-Lo against basic strategy.

This could also be integrated into the game, which could also help recommend betsize before each hand.

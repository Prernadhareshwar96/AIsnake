import game
import RLAgent
import Multigamer

#Multi Game Simulation
agent = RLAgent.RandomSnakeAgent()

#Mutligamer attributes:
# - numberOfParallelGames (no default)
# - RLAgent (no default)
# - numberOfTrials (default = 1)
# - numberOfIterations (default=1)
# - reward (default=100)
# - cost (default=1)
# - dim (default=(250,250))
gamer = Multigamer.multiGamer(10, agent,5,25)

gamer.runSimulation()
results = gamer.getResults()

## Single Game Simulation (with GUI)
# snake = game.Snake()
# foodSpawner = game.FoodSpawner()
# snakeGame = game.SnakeGame(snake, foodSpawner, 100, 1, True, (150,150))
# results = snakeGame.simulate(agent,5,3)

## Single Game Manual Play (with GUI)
# snake = game.Snake()
# foodSpawner = game.FoodSpawner()
# #snakeGame.play()
# #score, movements, food = snakeGame.getResults()
# print(results[0][10])
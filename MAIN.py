import game
import RLAgent

snake = game.Snake()
foodSpawner = game.FoodSpawner()
snakeGame = game.SnakeGame(snake, foodSpawner, 100, 1, True, (500,500))
agent = RLAgent.RandomSnakeAgent(snakeGame.getActions())
results = snakeGame.simulate(agent,1,3)
snakeGame.play()
score, movements, food = snakeGame.getResults()
print(results[0][10])
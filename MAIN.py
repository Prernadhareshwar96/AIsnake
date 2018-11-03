import game
import RLAgent

snake = game.Snake()
foodSpawner = game.FoodSpawner()
snakeGame = game.SnakeGame(snake, foodSpawner, 100, 1, True, (150,150))
agent = RLAgent.RandomSnakeAgent(snakeGame.getActions())
results = snakeGame.simulate(agent,1,3)
snakeGame.play()
score, movements, food = snakeGame.getResults()
print(results[0][10])
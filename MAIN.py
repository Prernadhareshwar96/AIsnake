import game
snake = game.Snake()
foodSpawner = game.FoodSpawner()
snakeGame = game.SnakeGame(snake, foodSpawner, 100, 1, True)
snakeGame.play()
score, movements, food = snakeGame.getResults()
print(score)
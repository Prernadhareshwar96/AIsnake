import pygame
import sys
import random
import GUI


class Snake():
    def __init__(self):
        self.position = [100, 50]
        self.body = [[100, 50], [90, 50], [80, 50]]
        self.direction = "RIGHT"
        self.numberOfMovements = 0

    def changeDirTo(self, dir):
        if dir == 'RIGHT' and not self.direction == 'LEFT':
            self.direction = 'RIGHT'
        if dir == 'LEFT' and not self.direction == 'RIGHT':
            self.direction = 'LEFT'
        if dir == 'UP' and not self.direction == 'DOWN':
            self.direction = 'UP'
        if dir == 'DOWN' and not self.direction == 'UP':
            self.direction = 'DOWN'

    def move(self, foodPos):
        if self.direction == 'RIGHT':
            self.position[0] += 10
        if self.direction == 'LEFT':
            self.position[0] -= 10
        if self.direction == 'UP':
            self.position[1] -= 10
        if self.direction == 'DOWN':
            self.position[1] += 10

        self.body.insert(0, self.position[:])
        self.numberOfMovements += 1

        if self.position == foodPos:
            return 1

        self.body.pop()
        return 0

    def getNumberOfMovements(self):
        return self.numberOfMovements

    def checkCollision(self, dim):
        # Wall collision
        if self.position[0] > (dim[0] - 10) or self.position[0] < 0:
            return 1

        if self.position[1] > (dim[1] - 10) or self.position[1] < 0:
            return 1

        # Self collision
        for bodyPart in self.body[1:]:
            if self.position[0] == bodyPart:
                return 1
        return 0

    def getHeadPos(self):
        return self.position

    def getBody(self):
        return self.body


class FoodSpawner():
    def __init__(self):
        self.position = [random.randrange(1, 50) * 10, random.randrange(1, 50) * 10]
        self.isFoodOnScreen = True
        self.numberOfFood = 0

    def getNumberOfFood(self):
        return self.numberOfFood

    def spawnFood(self):
        if self.isFoodOnScreen == False:
            self.position = [random.randrange(1, 50) * 10, random.randrange(1, 50) * 10]
            self.numberOfFood += 1
            self.isFoodOnScreen = True
        return self.position

    def setFoodOnScreen(self, b):
        self.isFoodOnScreen = b

    def getFoodPosition(self):
        return self.position


class SnakeGame():
    def __init__(self, snake, foodSpawner, reward=100, cost=1, display=True, dimensions=(500, 500)):
        self.score = 0
        self.snake = snake
        self.foodSpawner = foodSpawner
        self.reward = reward
        self.cost = cost
        self.GUI = None
        self.numberOfIters = 0
        self.dim = dimensions
        if display:
            self.GUI = GUI.SnakeGUI(self.dim)

    def getActions(self):
        return ['UP', 'LEFT', 'RIGHT', 'DOWN', 'NONE']

    def getState(self):
        return (self.snake.getBody(), self.foodSpawner.getFoodPosition(), self.dim)

    def gameOver(self):
        pygame.quit()
        sys.exit()

    def printStatus(self, gameOver=False):
        print('---------------------')
        if gameOver:
            print('GAME OVER')
        print('Score: ' + str(self.score))
        print('Number of Food Items:' + str(self.foodSpawner.getNumberOfFood()))
        print('Number of Movement Steps:' + str(self.snake.getNumberOfMovements()))
        print('---------------------')

    def getResults(self):
        return (self.score, self.snake.getNumberOfMovements(), self.foodSpawner.getNumberOfFood())

    def succAndProbReward(self, state, action):
        foodPos = state[1]
        snakebody = state[0]
        if action == 'RIGHT':
            self.snake.position[0] += 10
            if self.snake.position == foodPos:
                snakebody.insert(0, self.position[:])
                reward = self.score + self.reward
            else:
                snakebody.insert(0, self.position[:])
                snakebody.pop()
                reward = self.score + self.cost

        if action == 'LEFT':
            self.snake.position[0] -= 10
            if self.snake.position == foodPos:
                snakebody.insert(0, self.position[:])
                reward = self.score + self.reward
            else:
                snakebody.insert(0, self.position[:])
                snakebody.pop()
                reward = self.score + self.cost
        if action == 'UP':
            self.snake.position[1] -= 10
            if self.snake.position == foodPos:
                snakebody.insert(0, self.position[:])
                reward = self.score + self.reward
            else:
                snakebody.insert(0, self.position[:])
                snakebody.pop()
                reward = self.score + self.cost
        if action == 'DOWN':
            self.snake.position[1] += 10
            if self.snake.position == foodPos:
                snakebody.insert(0, self.position[:])
                reward = self.score + self.reward
            else:
                snakebody.insert(0, self.position[:])
                snakebody.pop()
                reward = self.score + self.cost

        new_state = snakebody
        prob = 1
        return (new_state, prob, reward)
        # rewards remaining

        # raise Exception ('Not implemented yet')
        return

    def reset(self):
        self.snake = Snake()
        self.score = 0
        self.numberOfIters = 0

    def simulate(self, RLAgent, numTrials=1, maxIterations=1):
        trialResults = []
        for trial in range(0, numTrials):
            results = []
            for iter in range(0, maxIterations):
                while True:
                    self.numberOfIters += 1

                    if not self.GUI == None:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                self.gameOver()

                    state = self.getState()
                    action = RLAgent.getAction(state)
                    if action != 'NONE':
                        self.snake.changeDirTo(action)

                    foodPos = self.foodSpawner.spawnFood()

                    if (self.snake.move(foodPos) == 1):
                        self.score += self.reward
                        self.foodSpawner.setFoodOnScreen(False)

                    if (self.snake.checkCollision(self.dim) == 1):
                        self.printStatus(True)
                        RLAgent.incorporateFeedback(state, action, self.score, [])
                        # self.gameOverSimul()
                        break

                    self.score -= self.cost
                    RLAgent.incorporateFeedback(state, action, self.score, self.getState())

                    if self.GUI != None:
                        self.GUI.update(self.snake.getBody(), self.foodSpawner.getFoodPosition(), self.score)
                results.append(self.score)
                self.reset()
            trialResults.append(results)
            self.reset()
        return trialResults

    def play(self):
        while True:
            self.numberOfIters += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameOver()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.snake.changeDirTo('RIGHT')

                    if event.key == pygame.K_LEFT:
                        self.snake.changeDirTo('LEFT')

                    if event.key == pygame.K_UP:
                        self.snake.changeDirTo('UP')

                    if event.key == pygame.K_DOWN:
                        self.snake.changeDirTo('DOWN')

            foodPos = self.foodSpawner.spawnFood()

            if (self.snake.move(foodPos) == 1):
                self.score += self.reward
                self.foodSpawner.setFoodOnScreen(False)

            if (self.snake.checkCollision(self.dim) == 1):
                self.printStatus(True)
                self.gameOver()
                break

            self.score -= self.cost

            if self.GUI != None:
                self.GUI.update(self.snake.getBody(), self.foodSpawner.getFoodPosition(), self.score)
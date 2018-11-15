import threading
import game

class gameThread (threading.Thread):
    def __init__(self, threadName, numberOfTrials, numberOfIterations, reward, cost, dim, RLAgent):
        threading.Thread.__init__(self)
        self.snake = game.Snake()
        self.foodSpawner = game.FoodSpawner()
        self.snakeGame = game.SnakeGame(self.snake, self.foodSpawner, reward, cost, False, dim)
        self.agent = RLAgent
        self.numberOfTrials = numberOfTrials
        self.numberOfIterations = numberOfIterations
        self.threadName = threadName
        self.results = None

    def run(self):
        print('Thread ' + str(self.threadName) + ' started!')
        self.agent.setActions(self.snakeGame.getActions())
        self.results = self.snakeGame.simulate(self.agent, self.numberOfTrials, self.numberOfIterations)

#Mutligamer attributes:
# - numberOfParallelGames (no default)
# - RLAgent (no default)
# - numberOfTrials (default = 1)
# - numberOfIterations (default=1)
# - reward (default=100)
# - cost (default=1)
# - dim (default=(250,250))

class multiGamer():
    def __init__(self, numberOfParallelGames, RLAgent, numberOfTrials=1, numberOfIterations=1, reward=100, cost=1, dim=(250,250)):
        self.noThreads = numberOfParallelGames
        self.reward = reward
        self.cost = cost
        self.dim = dim
        self.agent = RLAgent
        self.threadlist = []
        self.numberOfTrials = numberOfTrials
        self.numberOfIterations = numberOfIterations

    def runSimulation(self):
        for i in range(self.noThreads):
            threadName = "snakeGame_" + str(i)
            gThread = gameThread(threadName, self.numberOfTrials, self.numberOfIterations, self.reward, self.cost, self.dim, self.agent)
            gThread.start()
            self.threadlist.append(gThread)

        for t in self.threadlist:
            t.join()
        print('Simulation with ' + str(self.noThreads) + ' parallel games ended successfully')


    def getResults(self):
        results = {}
        for thread in self.threadlist:
            trial = -1
            for trialResults in thread.results:
                trial +=1
                iteration = -1
                for iterationResults in trialResults:
                    iteration += 1
                    results[(thread.threadName,trial,iteration)] = iterationResults
        return results
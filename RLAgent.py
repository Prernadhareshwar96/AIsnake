import random


class RLAgent:
    # Your algorithm will be asked to produce an action given a state.
    def setActions(self, actions): raise NotImplementedError("Override me")

    def getAction(self, state): raise NotImplementedError("Override me")

    # We will call this function when simulating an MDP, and you should update
    # parameters.
    # If |state| is a terminal state, this function will be called with (s, a,
    # 0, None). When this function is called, it indicates that taking action
    # |action| in state |state| resulted in reward |reward| and a transition to state
    # |newState|.
    def incorporateFeedback(self, state, action, reward, newState): raise NotImplementedError("Override me")


class RandomSnakeAgent(RLAgent):
    def __init__(self, actions=None):
        self.actions = actions

    def setActions(self, actions):
        self.actions = actions

    def getAction(self, state):
        return random.sample(self.actions, 1)[0]

    def incorporateFeedback(self, state, action, reward, newState):
        # random agent does not incorporate any feedback
        return


class chutiya(RLAgent):
    def __init__(self, actions, discount, featureExtractor, explorationProb=0.2):
        self.actions = actions
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = defaultdict(float)
        self.numIters = 0

    # Return the Q function associated with the weights and features
    def getQ(self, state, action):
        score = 0
        for f, v in self.featureExtractor(state, action):
            score += self.weights[f] * v
        return score

    # exploration strategy
    def getAction(self, state):
        self.numIters += 1
        if random.random() < self.explorationProb:
            return random.choice(self.actions(state))
        else:
            return max((self.getQ(state, action), action) for action in self.actions(state))[1]

    # Call this function to get the step size to update the weights.
    def getStepSize(self):
        return 1.0 / math.sqrt(self.numIters)

    # Feedback incorporating
    def incorporateFeedback(self, state, action, reward, newState):
        phi = self.featureExtractor(state, action)
        Q_val = self.getQ(state, action)
        if newState == None:
            for f, v in phi:
                self.weights[f] = self.weights[f] - self.getStepSize() * Q_val * v
        else:
            acts = self.actions(newState)
            V_opt = self.getQ(newState, acts[0])
            for a in acts:
                V_opt = max(V_opt, self.getQ(newState, a))
            for f, v in phi:
                self.weights[f] = self.weights[f] - self.getStepSize() * Q_val * v + self.getStepSize() * (
                            reward + self.discount * V_opt) * v

def snakeFeatureExtractor(state, action):
    # Feature Extractor should return distances into eight dimensions from the snakes head to....
    #  ...walls
    #  ...fruit
    #  ...self
    result = []
    result.append((state[0][0], action), 1)
    result.append((state[1], action), 1)
    result.append((state, action), 1)
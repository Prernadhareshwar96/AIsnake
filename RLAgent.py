import random
class RLAgent:
    # Your algorithm will be asked to produce an action given a state.
    def getAction(self, state): raise NotImplementedError("Override me")

    # We will call this function when simulating an MDP, and you should update
    # parameters.
    # If |state| is a terminal state, this function will be called with (s, a,
    # 0, None). When this function is called, it indicates that taking action
    # |action| in state |state| resulted in reward |reward| and a transition to state
    # |newState|.
    def incorporateFeedback(self, state, action, reward, newState): raise NotImplementedError("Override me")

class RandomSnakeAgent(RLAgent):
    def __init__(self, actions):
        self.actions = actions

    def getAction(self, state):
        return random.sample(self.actions,1)[0]

    def incorporateFeedback(self, state, action, reward, newState):
        #random agent does not incorporate any feedback
        return

def snakeFeatureExtractor(state, action):
    #Feature Extractor should return distances into eight dimensions from the snakes head to....
    #  ...walls
    #  ...fruit
    #  ...self
    raise Exception('Not implemented yet')
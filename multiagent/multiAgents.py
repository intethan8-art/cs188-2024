# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

       

        "*** YOUR CODE HERE ***"
        # 离Ghost远，离food近，考虑“无敌”状态
        score = currentGameState.getScore()

        foodList = newFood.asList()
        if foodList:
            minFoodDist = min(manhattanDistance(newPos, f) for f in foodList)
            score += 10.0 / (minFoodDist + 1)

        for ghost in newGhostStates:
            dist = manhattanDistance(newPos, ghost.getPosition())
            if ghost.scaredTimer > 0:
                score += 5.0 / (dist + 1)
            else:
                if dist < 2:
                    score -= 1000
                else:
                    score -= 2.0 / dist
        
        score -= 4 * len(foodList)

        return score

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        num = gameState.getNumAgents()
        def helper_eval(state: GameState, cur_depth, index) :

            if state.isWin() or state.isLose() :
                return self.evaluationFunction(state)
            if cur_depth == self.depth :
                return self.evaluationFunction(state)
            elif index == 0 :
                return max_eval(state, cur_depth, index)
            else :
                return min_eval(state, cur_depth, index)
            
        def max_eval(state, cur_depth, index) :
            v = float("-inf")
            actions = state.getLegalActions(index)
            for action in actions :
                suc_state = state.generateSuccessor(index, action)
                v = max(v, helper_eval(suc_state, cur_depth, (index + 1) % num))
            return v

        def min_eval(state, cur_depth, index) :
            v = float("inf")
            actions = state.getLegalActions(index)
            for action in actions :
                suc_state = state.generateSuccessor(index, action)
                next_index = (index + 1) % num
                next_depth = cur_depth + 1 if next_index == 0 else cur_depth
                v = min(v, helper_eval(suc_state, next_depth, next_index))
            return v

        bestAction = None
        bestValue = float("-inf")

        for action in gameState.getLegalActions(0):
            succ = gameState.generateSuccessor(0, action)
            value = helper_eval(succ, 0, 1)

            if value > bestValue:
                bestValue = value
                bestAction = action

        return bestAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        num = gameState.getNumAgents()
        def helper_eval(state: GameState, cur_depth, index, alpha, beta) :

            if state.isWin() or state.isLose() :
                return self.evaluationFunction(state)
            if cur_depth == self.depth :
                return self.evaluationFunction(state)
            elif index == 0 :
                return max_eval(state, cur_depth, index, alpha, beta)
            else :
                return min_eval(state, cur_depth, index, alpha, beta)
            
        def max_eval(state, cur_depth, index, alpha, beta) :
            v = float("-inf")
            actions = state.getLegalActions(index)
            for action in actions :
                suc_state = state.generateSuccessor(index, action)
                v = max(v, helper_eval(suc_state, cur_depth, (index + 1) % num, alpha, beta))
                if v > beta:
                    return v

                alpha = max(alpha, v)
            return v

        def min_eval(state, cur_depth, index, alpha, beta) :
            v = float("inf")
            actions = state.getLegalActions(index)
            for action in actions :
                suc_state = state.generateSuccessor(index, action)
                next_index = (index + 1) % num
                next_depth = cur_depth + 1 if next_index == 0 else cur_depth
                v = min(v, helper_eval(suc_state, next_depth, next_index, alpha, beta))

                if v < alpha:
                    return v

                beta = min(beta, v)

            return v

        bestAction = None
        bestValue = float("-inf")
        alpha = float('-inf')
        beta = float('inf')

        for action in gameState.getLegalActions(0):
            succ = gameState.generateSuccessor(0, action)
            value = helper_eval(succ, 0, 1, alpha, beta)

            if value > bestValue:
                bestValue = value
                bestAction = action

            alpha = max(alpha, value)

        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        num = gameState.getNumAgents()
        def helper_eval(state: GameState, cur_depth, index) :

            if state.isWin() or state.isLose() :
                return self.evaluationFunction(state)
            if cur_depth == self.depth :
                return self.evaluationFunction(state)
            elif index == 0 :
                return max_eval(state, cur_depth, index)
            else :
                return expecti_eval(state, cur_depth, index)
            
        def max_eval(state, cur_depth, index) :
            v = float("-inf")
            actions = state.getLegalActions(index)
            for action in actions :
                suc_state = state.generateSuccessor(index, action)
                v = max(v, helper_eval(suc_state, cur_depth, (index + 1) % num))
            return v

        def expecti_eval(state, cur_depth, index) :
            actions = state.getLegalActions(index)
            length = len(actions)
            v = 0
            for action in actions :
                suc_state = state.generateSuccessor(index, action)
                next_index = (index + 1) % num
                next_depth = cur_depth + 1 if next_index == 0 else cur_depth
                v = v + helper_eval(suc_state, next_depth, next_index)
            return v / length

        bestAction = None
        bestValue = float("-inf")

        for action in gameState.getLegalActions(0):
            succ = gameState.generateSuccessor(0, action)
            value = helper_eval(succ, 0, 1)

            if value > bestValue:
                bestValue = value
                bestAction = action

        return bestAction


def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).
    DESCRIPTION: 
      features -- dist from Ghost, dist from nearest food, scared time, remaining food
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    score = currentGameState.getScore()

    foodList = newFood.asList()
    if foodList:
        minFoodDist = min(manhattanDistance(pos, f) for f in foodList)
        score += 50.0 / (minFoodDist + 1)

    for ghost in newGhostStates:
        dist = manhattanDistance(pos, ghost.getPosition())
        if ghost.scaredTimer > 0:
                score += 5.0 / (dist + 1)
        else:
            if dist < 2:
                score -= 1000
            else:
                score -= 2.0 / dist
        
    score -= 4 * len(foodList)

    return score



# Abbreviation
better = betterEvaluationFunction

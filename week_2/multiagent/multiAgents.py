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

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        bestScore = -999999.0
        bestAction = None

        for action in legalMoves:
            score = self.evaluationFunction(gameState, action)
            print action, score
            if score > bestScore:
                bestScore = score
                bestAction = action
#        bestScore = max(scores)
#        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
#        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        print "--------------------------\n"
#        print bestScore, bestAction
#        return legalMoves[chosenIndex]
        return bestAction

    def evaluationFunction(self, currentGameState, action):
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

        score = 0
        for ghost_pos in successorGameState.getGhostPositions():
            dis = manhattanDistance(newPos, ghost_pos)
            if dis <= 0:
                return -999.0

        food_grid =  successorGameState.getFood()

        for x in range(food_grid.width):
            for y in range(food_grid.height):
                if food_grid[x][y] is True:
                    dis = manhattanDistance(newPos, [x,y])
                    if dis == 0:
                        score += 10000
                        continue
                    score += (1/dis)

#        score += successorGameState.getScore()
        return score

def scoreEvaluationFunction(currentGameState):
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
##########################################
#Mycode Minimax
    def mini(self, state, agent, depth, num_agents):

        actions = state.getLegalActions(agent)

        best = 9999999
        mini_act = None
        for action in actions:
            child = state.generateSuccessor(agent, action)
            value, last_act = self.minimax_rec(child, agent, depth, num_agents)
            if value < best:
                best = value
                mini_act = action
        return best, mini_act

    def maxi(self, state, agent, depth, num_agents):

        actions = state.getLegalActions(agent)
        print actions
        best = -9999999
        maxi_act = None
        for action in actions:
            child = state.generateSuccessor(agent, action)
            value, last_act = self.minimax_rec(child, agent, depth, num_agents)
            if value >= best :
                best = value
                maxi_act = action
        return best, maxi_act

    def minimax_rec(self, state, agent, depth, num_agents):

        agent = (agent + 1) % num_agents

        if agent == 0:
            depth -= 1
#        print agent
        actions = state.getLegalActions(agent)
        if len(actions) == 0  or depth < 0 :
            return self.evaluationFunction(state), 'Stop'

        if agent == 0:
            return self.maxi(state, agent, depth, num_agents)
        else:
            return self.mini(state, agent, depth, num_agents)

    def getAction(self, gameState):
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
        """
        "*** YOUR CODE HERE ***"
        num_agents = gameState.getNumAgents()
        value, action =  self.minimax_rec(gameState, -1, self.depth, num_agents)
        print action, value

        return action
#        util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
###############################################################
#Mycode Alpha-Beta
    def mini(self, state, agent, depth, num_agents, alpha, beta):

        actions = state.getLegalActions(agent)
        mini_act = None
        best_for_this_node = +999999.0
	
        for action in actions:
            child = state.generateSuccessor(agent, action)
            value, last_act = self.alpha_beta(child, agent, depth, num_agents, alpha, beta)

            #Prunning can be done at <= alpha, but to satisfy Question Q3 ans, using <
            if value < alpha:
                return value, action
            if value < best_for_this_node:
                best_for_this_node = value
                mini_act = action
            if value < beta:
                beta = value

        return best_for_this_node, mini_act

    def maxi(self, state, agent, depth, num_agents, alpha, beta):

        actions = state.getLegalActions(agent)
        maxi_act = None
        best_for_this_node = -999999.0

        for action in actions:
            child = state.generateSuccessor(agent, action)
            value, last_act = self.alpha_beta(child, agent, depth, num_agents, alpha, beta)

            #Prunning can be done at >= beta, but to satisfy Question Q3 ans, using >
            if value > beta:
                return value, action
            if value > best_for_this_node:
                best_for_this_node = value
                maxi_act = action
            if value > alpha:
                alpha = value

        return best_for_this_node, maxi_act

    def alpha_beta(self, state, agent, depth, num_agents, alpha, beta):

        agent = (agent + 1) % num_agents

        if agent == 0:
           depth -= 1

        actions = state.getLegalActions(agent)
        if len(actions) == 0:
            return float(self.evaluationFunction(state)), 'Stop'
        if depth < 0 :
            return float(self.evaluationFunction(state)), 'Stop'

        if agent == 0:
            return self.maxi(state, agent, depth, num_agents, alpha, beta)
        else:
            return self.mini(state, agent, depth, num_agents, alpha, beta)

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        num_agents = gameState.getNumAgents()
        alpha = -999999.0
        beta  = +999999.0
        value, action =  self.alpha_beta(gameState, -1, self.depth, num_agents, alpha, beta)
#        print action, value

        return action

#        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
#Mycode Expectimax
    def expecti(self, state, agent, depth, num_agents):

        expecti_value = 0.0
        expecti_act = None
        actions = state.getLegalActions(agent)
        prob = 1.0 / float(len(actions)) #Assuming uniform distribution of actions

        for action in actions:
            child = state.generateSuccessor(agent, action)
            value, last_act = self.expectimax(child, agent, depth, num_agents)
            expecti_value += (prob * value)

        return expecti_value, action
#action is of no use here, as root always be max agent and we take weighted avg of all actions outcomes from expecti agent next move.

    def maxi(self, state, agent, depth, num_agents):

        actions = state.getLegalActions(agent)
#        print actions
        best = -9999999
        maxi_act = None

        for action in actions:
            child = state.generateSuccessor(agent, action)
            value, last_act = self.expectimax(child, agent, depth, num_agents)
            if value >= best :
                best = value
                maxi_act = action

        return best, maxi_act

    def expectimax(self, state, agent, depth, num_agents):

        agent = (agent + 1) % num_agents

        if agent == 0:
            depth -= 1
#        print agent
        actions = state.getLegalActions(agent)
        if len(actions) == 0  or depth < 0 :
            return self.evaluationFunction(state), 'Stop'

        if agent == 0:
            return self.maxi(state, agent, depth, num_agents)
        else:
            return self.expecti(state, agent, depth, num_agents)

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        num_agents = gameState.getNumAgents()
        value, action =  self.expectimax(gameState, -1, self.depth, num_agents)
#        print action, value

        return action

#        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction


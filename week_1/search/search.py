# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

class Node:

	def __init__(self, state, parent,cost,last_action, priority):
		self.state = state
		self.parent = parent
		self.cost = cost
		self.last_action = last_action
		self.priority = priority

def give_actions(N):
	
	act = []
	while N.last_action is not None:
		act.insert(0, N.last_action)
		N = N.parent
#	print "action list is ", act
	return act

def search_actions(problem, alg, heur=None):
	priority = 0
	inc_priority = 0
	if alg is 'dfs':
		inc_priority = -1
	elif alg is 'bfs':
		inc_priority = 1


#	if type(problem).__name__ is 'CornersProblem':
	if True:
		actlist = []

	start = problem.getStartState()
	print problem.getStartState()
	explored = dict()

	que = util.PriorityQueue()
	start_node = Node(start, None, 0, None, priority)
	que.update(start_node,  start_node.priority)
	"""
	actlist = ['North', 'East', 'East', 'North', 'West', 'West', 'West', 'West', 'West', 'West', 'South', 'South', 'South', 'South', 'East', 'East', 'South', 'South', 'West', 'West', 'West', 'South', 'South', 'East', 'East', 'East','North', 'East', 'East', 'North', 'West', 'West', 'West', 'West', 'West', 'West', 'South', 'South', 'South', 'South', 'East', 'East', 'South', 'South', 'West', 'West', 'West', 'South', 'South', 'East', 'East', 'East']

	return actlist
	"""
	while True:
		if que.isEmpty():
			return None
		else:
			state_expl = que.pop()
#			print "state popped \n", state_expl.state
			if explored.has_key(state_expl.state):
				continue
			if True:
#			if type(problem).__name__ is 'CornersProblem':
#				print "corner problem"
				res = problem.isGoalState(state_expl.state)
				if res is 4:
					actlist.extend(give_actions(state_expl))
					print actlist
					return actlist
				elif res is 1:
					actlist.extend(give_actions(state_expl))
					explored.clear()
					
			elif problem.isGoalState(state_expl.state):
				return give_actions(state_expl)
			
			if alg is not 'ucs':
				priority = state_expl.priority + inc_priority
			for child, act, cost in problem.getSuccessors(state_expl.state):
				if not explored.has_key(child):

					n = Node(child, state_expl, cost, act, priority)
					if alg is 'ucs':
						priority = problem.getCostOfActions(give_actions(n))
						n.priority = priority;
					elif alg is 'astar':
						priority = problem.getCostOfActions(give_actions(n)) + heur(child, problem)
						n.priority = priority;
					
					que.update(n, n.priority)

			explored[state_expl.state] = state_expl
	

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    print "start" , problem.getStartState()
 
#    util.raiseNotDefined()
   
    return search_actions(problem, 'dfs')
	          	

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
#    util.raiseNotDefined()

    return search_actions(problem, 'bfs')

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
#    util.raiseNotDefined()

    return search_actions(problem, 'ucs')

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
#    util.raiseNotDefined()

    return search_actions(problem, 'astar', heuristic)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

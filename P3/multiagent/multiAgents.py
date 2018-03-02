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
import random, util, sys

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
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

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
        '''
        python pacman.py -p ReflexAgent -l testClassic
        Try out your reflex agent on the default mediumClassic layout with one ghost or two (and animation off to speed up the display):

        python pacman.py --frameTime 0 -p ReflexAgent -k 1
        python pacman.py --frameTime 0 -p ReflexAgent -k 2
        '''

        "*** YOUR CODE HERE ***"
        remainingFood = newFood.asList()

        maxScore = sys.maxint
        
        if  len(remainingFood) == 0: #Finished if no food left.
          return maxScore
        
        closer_food = min([util.manhattanDistance(newPos, food) for food in remainingFood]) #Get the closest dot of food and its distance to the player

        for ghost in newGhostStates:#Get the closest ghost and its distance to the player
          ghostPos = ghost.getPosition()
          closer_ghost = min([util.manhattanDistance(newPos, ghostPos) for ghost in newGhostStates])

        score = successorGameState.getScore() + (closer_ghost - closer_food)#Computing the score taking into account only the closest food and closest ghost.
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

    def minPacman(self, gameState, depth, numGhost): #Recursive function that computes the minimum rewarded state of an agent, normally used for the ghosts.

        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)

        actions = gameState.getLegalActions(numGhost)
        score = float('inf')

        for action in actions:
            if numGhost == gameState.getNumAgents() - 1:
                nextStateMove = gameState.generateSuccessor(numGhost, action)
                score = min(score, self.maxPacman(nextStateMove, depth + 1))

            else:
                nextStateMove = gameState.generateSuccessor(numGhost, action)
                score = min(score, self.minPacman(nextStateMove, depth, numGhost + 1))

        return score


    def maxPacman(self, gameState, depth): # Recursive function that computes the maximum rewarced state of an agent, normally for the pacman.

        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)

        actions = gameState.getLegalActions(0)
        score = float('-inf')

        for action in actions:
            nextStateMove = gameState.generateSuccessor(0, action)
            score = max(score, self.minPacman(nextStateMove, depth, 1))

        return score

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

        pacman = 0
        initialGhost = 1
        initialDepth = 0
        actions = gameState.getLegalActions(pacman)

        best_action = None
        score = float('-inf')

        for action in actions:
            nextState = gameState.generateSuccessor(pacman, action)
            prev_score = score
            score = max(score, self.minPacman(nextState, initialDepth, initialGhost))#Starting the recursivity with min method of minimax.
            if score > prev_score: #Getting the action with best score.
                best_action = action

        return best_action

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent): #Same execution of the minimaz agent, adding the alpha and beta parameters, using to compare the socre with them in each execution of the recursive methods.
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def minPacman(self, gameState, depth, numGhost, alpha, beta):

        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)

        actions = gameState.getLegalActions(numGhost)
        score = float('inf')

        for action in actions:
            if numGhost == gameState.getNumAgents() - 1:
                nextStateMove = gameState.generateSuccessor(numGhost, action)
                score = min(score, self.maxPacman(nextStateMove, depth + 1, alpha, beta))

            else:
                nextStateMove = gameState.generateSuccessor(numGhost, action)
                score = min(score, self.minPacman(nextStateMove, depth, numGhost + 1, alpha, beta))

            beta = min(beta, score)

            if score < alpha:
                break

        return score


    def maxPacman(self, gameState, depth, alpha, beta):

        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)

        actions = gameState.getLegalActions(0)
        score = float('-inf')

        for action in actions:
            nextStateMove = gameState.generateSuccessor(0, action)
            score = max(score, self.minPacman(nextStateMove, depth, 1, alpha, beta))
            alpha = max(alpha, score)

            if score > beta:
                break

        return score

    def getAction(self, gameState):

        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        pacman = 0
        initialGhost = 1
        initialDepth = 0
        actions = gameState.getLegalActions(pacman)

        best_action = None
        score = float('-inf')

        alpha = float('-inf')
        beta = float('inf')

        for action in actions:
            nextState = gameState.generateSuccessor(pacman, action)
            prev_score = score
            score = max(score, self.minPacman(nextState, initialDepth, initialGhost, alpha, beta))
            '''if score > prev_score:
                best_action = action'''

            if score > alpha:
                alpha = score
                best_action = action

        return best_action

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

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


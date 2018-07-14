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

        print "newPos= ", newPos

        "*** YOUR CODE HERE ***"

        ghostDistance=0
        gd=[]
        for ghostState in newGhostStates:
            ghostPos=ghostState.getPosition()
            tmpDist = (abs(newPos[0]-ghostPos[0])+abs(newPos[1]-ghostPos[1]))
            if tmpDist == 0:
                return -2
            ghostDistance += tmpDist
            gd.append(ghostDistance)

        #print "ghostDist", ghostDistance
        ghostDistance /= len(newGhostStates)


        foods= list(newFood)
        x= len(foods)
        y= len(foods[0])

        minFoodDist = 100000
        foodCount=0
        oldFoodCount=0
        oldFood=currentGameState.getFood()

        for i in range(0,x):
            for j in range(0,y):
                if newFood[i][j]:
                    foodCount += 1
                    foodDist = abs(newPos[0]-i)+abs(newPos[1]-j)
                    if foodDist < minFoodDist and foodDist != 0:
                        minFoodDist = foodDist

                if currentGameState.hasFood(i,j):
                    oldFoodCount += 1

        #this is the last food: eat it
        if minFoodDist == 100000:
            minFoodDist = 0

        foodCount=abs(foodCount-oldFoodCount)

        rowXCol=(x-2)*(y-2)
        #print foodCount, rowXCol, ghostDistance, minFoodDist
        normFoodCount = float(foodCount)
        normGhostDist= float(ghostDistance)/((x-2-1)+(y-2-1))
        normFoodDist = float(minFoodDist)/((x-2-1)+(y-2-1))

        #print "fc=", foodCount, "minFoodDist=",minFoodDist, "ghostDistance", ghostDistance

        #ghost distance is too far so it doesn't matter
        if ghostDistance >= 5:
            normGhostDist = 0

        #some ghost is too close: so run
        for dist in gd:
            if dist <= 1:
                normGhostDist = -2

        #print "nfc=", float(float(normFoodCount)), "nfd=", (1-float(normFoodDist)), "ngd=", (float(normGhostDist))

        if newPos == currentGameState.getPacmanPosition():
            return float(float(normFoodCount) + (1-float(normFoodDist)) + (float(normGhostDist))) - 0.4
        else:
            return float(
                float(normFoodCount) + (1-float(normFoodDist)) + (float(normGhostDist)))

        return successorGameState.getScore()

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

    def minimax(self, gameState, isPac, ghostNum, depth):

        numAgents = gameState.getNumAgents()
        if depth == self.depth*numAgents:#or terminal position reached check for that:
            return self.evaluationFunction(gameState)

        if isPac:
            legalMoves = gameState.getLegalActions(0)
            if len(legalMoves)!=0:
                scores = [self.minimax(gameState.generateSuccessor(0, action), False, 1, depth+1) for action in legalMoves]
                print scores
                maxScore, maxAction = scores[0]
                for score,act in scores:
                    if score>maxScore:
                        maxScore=score
                        maxAction=act
                return maxScore,maxAction
            else:
                return self.evaluationFunction(gameState)

        if not isPac:
            #check comparison with ghostNum
            legalMoves = gameState.getLegalActions(ghostNum)
            if len(legalMoves)!=0:
                #numAgents = gameState.getNumAgents()
                if ghostNum<gameState.getNumAgents()-1:
                    scores = [self.minimax(gameState.generateSuccessor(ghostNum, action), False, ghostNum+1, depth+1) for action in legalMoves]
                    minScore, minAction = scores[0]
                    for score, act in scores:
                        if score < minScore:
                            minScore = score
                            minAction = act
                    return minScore, minAction
                else:
                    scores = [self.minimax(gameState.generateSuccessor(ghostNum, action), True, 0, depth+1) for action in legalMoves]
                    minScore, minAction = scores[0]
                    for score, act in scores:
                        if score < minScore:
                            minScore = score
                            minAction = act
                    return minScore, minAction
            else:
                return self.evaluationFunction(gameState)


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

        #print self.evaluationFunction(gameState)
        score, action = self.minimax(gameState, True, 0, 0)
        print score
        return action

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
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


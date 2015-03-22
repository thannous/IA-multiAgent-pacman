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
from operator import or_
from random import betavariate

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
        legalMoves.remove('Stop')
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
        distanceList = []
        # Useful information you can extract from a GameState (pacman.py)
        previousState = currentGameState
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        lastFood = previousState.getFood()
        
        newPos = successorGameState.getPacmanPosition()
        for x in range(lastFood.width):
            for y in range(lastFood.height):
                if lastFood[x][y] == True:
                    if newPos != (x,y):
                        distanceList.append(manhattanDistance(newPos, (x,y)))
                        
       
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        capsulePos = successorGameState.getCapsules()     
        distPacmanGhost = manhattanDistance(newPos, newGhostStates[0].getPosition())
        
  
        if newScaredTimes[0] > 0 :
            distanceList.append(distPacmanGhost)
        "*** YOUR CODE HERE ***"
        
     
        point = 0

                    
        #distanceList.append(manhattanDistance(newPos, list(capsulePos[0])))                                
        if distPacmanGhost < 2:
            if newScaredTimes[0] > 0:
                return successorGameState.getScore() + 1/min(distanceList)  
            else:
                return -9999
        if len(distanceList) == 0:
            return successorGameState.getScore()  
        return successorGameState.getScore() + 1/min(distanceList)

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

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
       
        def maxValue(gameState,profondeur, numGhost):
            #print 'MAX'
            maxScore = -(float("inf"))
           
            if gameState.isWin() or gameState.isLose() or profondeur == 0:
                #print profondeur
                #print "eval max", self.evaluationFunction(gameState)
                return self.evaluationFunction(gameState)
            
            legalsAction = gameState.getLegalActions(0)
            for action in legalsAction:
                successorGameState = gameState.generateSuccessor(0, action)
                score = minValue(successorGameState ,profondeur, 1 , numGhost)
                if maxScore < score:
                    maxScore = score
            #print " c max", maxScore    
            return maxScore
        
        def minValue (gameState, profondeur,agentIndex, numGhost):
            
            minScore = float("inf")
            legalsAction = gameState.getLegalActions(agentIndex)
            #print 'MIN'
            """print 'legalAction ', legalsAction
            print 'self depth', self.depth
            print 'agent Index', agentIndex 
            print 'numAgents', numAgents"""
            if gameState.isWin() or gameState.isLose() or profondeur == 0:
                #print "===============" ,self.evaluationFunction(gameState)
                return self.evaluationFunction(gameState)
            for action in legalsAction:
                successorGameState = gameState.generateSuccessor(agentIndex, action)
                """print "numagent :",numAgents
                print "agentIndex ", agentIndex"""
                if agentIndex  == numGhost:
                    #print "TRUE"
                    score = maxValue(successorGameState, profondeur - 1,numGhost)
                else :
                    score =  minValue(successorGameState,profondeur, agentIndex + 1,numGhost)
                if minScore > score:
                    minScore = score
      
             
                
            return minScore
    
        numAgents = gameState.getNumAgents()
        numGhost = numAgents - 1
        
        legalmoves = gameState.getLegalActions(0)
        maxScore = -(float("inf"))
        bestMove = "Stop"
        #print "------------"    
        for action in legalmoves:
            successorGameState = gameState.generateSuccessor(0, action)
            score =  minValue(successorGameState, self.depth, 1 ,numGhost)
            #print score
            if (maxScore <  score ):
                    maxScore = score
                    bestMove = action 
        return bestMove
        
        

class AlphaBetaAgent(MultiAgentSearchAgent):

    def getAction(self, gameState):
        score = -(float("inf"))
        alpha = -(float("inf"))
        beta = float("inf")
        numAgents = gameState.getNumAgents()
        numGhost = numAgents - 1
        legalmoves = gameState.getLegalActions(0)
        bestMove = "Stop"
        
        def maxValue(gameState,profondeur, numGhost, alpha, beta):
            #print 'MAX'
            score = -(float("inf"))
           
            if gameState.isWin() or gameState.isLose() or profondeur == 0:
                #print profondeur
                #print "eval max", self.evaluationFunction(gameState)
                return self.evaluationFunction(gameState)
            
            legalsAction = gameState.getLegalActions(0)
            for action in legalsAction:
                successorGameState = gameState.generateSuccessor(0, action)
                score = max( score , minValue(successorGameState ,profondeur, 1 , numGhost,alpha, beta ))
                if score > beta :
                    return score
                alpha = max(alpha, score)
            return score
        
        """ Trouve le min des noeuf-fils"""
        def minValue (gameState, profondeur,agentIndex, numGhost, alpha , beta):
            
            score = float("inf")
            legalsAction = gameState.getLegalActions(agentIndex)
            #print 'MIN'
            """print 'legalAction ', legalsAction
            print 'self depth', self.depth
            print 'agent Index', agentIndex 
            print 'numAgents', numAgents"""
            if gameState.isWin() or gameState.isLose() or profondeur == 0:
                #print "===============" ,self.evaluationFunction(gameState)
                return self.evaluationFunction(gameState)
            for action in legalsAction:
                successorGameState = gameState.generateSuccessor(agentIndex, action)
                """print "numagent :",numAgents
                print "agentIndex ", agentIndex"""
                #print "==============="
                if agentIndex  == numGhost:
                    score = min(score, maxValue(successorGameState, profondeur - 1,numGhost, alpha, beta))
                    """print "****alpha :", alpha
                    print "****beta :", beta
                    print "****min :", score"""
                else :
                    score = min(score, minValue(successorGameState,profondeur, agentIndex + 1,numGhost,alpha, beta))
                    """print "*min :", score"""
                if score < alpha:
                    return score
                beta = min(beta, score)
            return score
    
   
        """
            Cherche la meilleur action pour chaque actions de pacman possibles ( aller en haut, en bas , ne pas
            bouger, etc ...
        """ 
        for action in legalmoves:
            successorGameState = gameState.generateSuccessor(0, action)
            #print score
            prevscore = score
            score = max(score, minValue(successorGameState, self.depth, 1 ,numGhost, alpha, beta))
            
            if (prevscore <  score ):
                    bestMove = action
            alpha = max(alpha, score)
        return bestMove

class ExpectimaxAgent(MultiAgentSearchAgent):

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


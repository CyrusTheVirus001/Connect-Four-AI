# -*- coding: utf-8 -*-
"""Connect_Four_AI_v03_Master.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DZ_zJUzhVx_IRU3zdpX8cQdQ7YQBW2qT
"""

#SHELDON SLATER
#810865586
#CONNECT FOUR AI

import json
import random
import sys
import copy

def valid_moves(precept):
    grid = precept['grid']
    moves = []
    for i, col in enumerate(grid):
        if col[0] == 0:
            moves.append(i)
    # moves = [i for i, col in enumerate(grid) if col[0] == 0]
    return moves

def Generate_Board(height,length):
  board = [[0 for col in range(height)] for row in range(length)]
  return board

def valid_moves1(Current_Board):
  moves = []
  for i,col in enumerate(Current_Board):
    if col[0] == 0: moves.append(i)
  return moves

def check_for_winner(player,CB):
  #Check Horizontal
  for j in range(len(CB[0])-3):
    for i in range(len(CB)):
      if(CB[i][j]==player & CB[i][j+1] == player & CB[i][j+2] == player & CB[i][j+3] == player):
        return True
  #Check Verticle
  for i in range(len(CB)-3):
    for j in range(len(CB[0])):
      if(CB[i][j]==player & CB[i+1][j] == player & CB[i+2][j] == player & CB[i+3][j] == player):
        return True
  #Check Diagonal
  for i in range(3,len(CB)):
    for j in range(len(CB[0])-3):
      if(CB[i][j]==player & CB[i-1][j+1] == player & CB[i-2][j+2] == player & CB[i-3][j+3] == player):
        return True
  #Check Diagonal
  for i in range(3,len(CB)):
    for j in range(3,len(CB[0])):
      if(CB[i][j]==player & CB[i-1][j-1] == player & CB[i-2][j-2] == player & CB[i-3][j-3] == player):
        return True
  return False


def apply_move(col,player,Current_Board):
  newBoard = copy.deepcopy(Current_Board)
  for i,slot in enumerate(newBoard[col]):
    if(slot != 0): 
      newBoard[col][i-1]=player
      return newBoard
  newBoard[col][-1]=player
  return newBoard

#
def CalculateCost(board_state,maxPlayer):
  length = len(board_state)
  height = len(board_state[0])
  rowOpportunities = (length%4)+1
  heightOpportunities = (height%4)+1

  total_Opportunities_Opp = rowOpportunities*height + heightOpportunities*length
  total_Opportunities_AI = total_Opportunities_Opp

  for row in range(length):
    row_count_opp = rowOpportunities
    row_count_AI = row_count_opp
    for cell in range(height):
      if(board_state[row][cell] == 1):
        row_count_opp = abs(row_count_opp-(cell+1))
        if row_count_opp <= 0:
          row_count_opp = 0
      elif(board_state[row][cell] == 2):
        row_count_AI = abs(row_count_AI-(cell+1))
        if row_count_AI <= 0:
          row_count_AI = 0

    total_Opportunities_Opp-=(rowOpportunities-row_count_opp)
    total_Opportunities_AI-=(rowOpportunities-row_count_AI)

  if(maxPlayer == 1):
    cost = total_Opportunities_AI-total_Opportunities_Opp
  else:
    cost = total_Opportunities_Opp-total_Opportunities_AI

  return cost/100

#Run random simulations of current game state till the end 
#and return winning statistics
def Poor_Monte_Carlo_Simulation(boardstate,maxPlayer):

  player_1_wins = 0
  player_2_wins = 0
  draws = 0

  iterations = 11
  Total_Games = 11
  while(iterations > 0):

    GameBoard = copy.deepcopy(boardstate)
    player = 2
    gameover = False
    iterations-=1

    while(gameover==False):

      if check_for_winner(1,GameBoard):
        player_1_wins+=1
        gameover = True
        break
      elif check_for_winner(2,GameBoard):
        player_2_wins+=1
        gameover = True
        break

      moves = valid_moves1(GameBoard)
      if(len(moves)==0):
        draws+=1
        gameover = True
        break

      move = random.choice(moves)
      GameBoard = apply_move(move,player,GameBoard)
      if player == 1: player = 2
      else: player = 1
  if(maxPlayer == 1):
    return player_1_wins/Total_Games
  else:
    return player_2_wins/Total_Games

#INITIAL STATES/SETUP
#alpha = float('-inf')
#beta = float('inf')
#player = 1
def Traverse_States(player,alpha,beta,current_board,depth,playerID):

  alpha_current = alpha
  beta_current = beta

  #Set the current cost of the node based on whether we are the minimizing or maximizing agent
  #Player 1 is Maximizing
  #Player 2 is Minimizing
  if(playerID == 1):
    if player == 1: 
      current_cost = float('-inf')
      next_player = 2
    else: 
      current_cost = float('inf')
      next_player = 1
  #Player 2 is Maximizing
  #Player 1 is Minimizing
  else:
    if player == 2: 
      current_cost = float('-inf')
      next_player = 1
    else: 
      current_cost = float('inf')
      next_player = 2


  #Check if Current Game State is a win or loss
  #Check if depth has been reached and return a Cost based on Heuristics
  #Player 1 is Maximizing
  if(playerID == 1):
    if check_for_winner(1, current_board): return 1000,0
    elif check_for_winner(2, current_board): return -1000,0
    if depth == 0: return (Poor_Monte_Carlo_Simulation(current_board,playerID)+CalculateCost(current_board,playerID)),0
  else:
    if check_for_winner(1, current_board): return -1000,0
    elif check_for_winner(2, current_board): return 1000,0
    if depth == 0: return (Poor_Monte_Carlo_Simulation(current_board,playerID)+CalculateCost(current_board,playerID)),0

  possible_moves = valid_moves1(current_board)
  best_move = possible_moves[0]

  #For every possible move, explore a new state of the game
  #Evaluate Returned Costs and determine if new states should be explored based on alpha-beta results
  for move in possible_moves:

    returned_cost,last_move = Traverse_States(next_player,alpha,beta,apply_move(move,player,current_board),depth-1,playerID)

    #Determine Cost and Alpha Results for Maximizing Player
    #If current beta is less than or equal to Alpha, break out of 'move loop'
    #Player 1 is Maximizing
    if(playerID == 1):
      if player == 1:
        if returned_cost > current_cost: 
          current_cost = returned_cost
          best_move = move
        if current_cost > alpha: alpha = current_cost
        if beta <= alpha: break

      #Determine Cost and Beta Results for Minimizing Player
      #If current beta is less than or equal to alpha, break out of 'move loop'
      else:
        if returned_cost < current_cost: current_cost = returned_cost
        if current_cost < beta: beta = current_cost
        if beta <= alpha: break
    #Player 2 is Maximizing
    else:
      if player == 2:
        if returned_cost > current_cost: 
          current_cost = returned_cost
          best_move = move
        if current_cost > alpha: alpha = current_cost
        if beta <= alpha: break

      #Determine Cost and Beta Results for Minimizing Player
      #If current beta is less than or equal to alpha, break out of 'move loop'
      else:
        if returned_cost < current_cost: current_cost = returned_cost
        if current_cost < beta: beta = current_cost
        if beta <= alpha: break

  #return current cost and current best move
  return current_cost,best_move









def main():
    print('Connect Four in Python', file=sys.stderr)
    for line in sys.stdin:
        print(line, file=sys.stderr)
        precept = json.loads(line)
        grid = precept['grid']
        player_ID = precept['player']
        cost,move = Traverse_States(player_ID,float('-inf'),float('inf'),grid,5,player_ID)
        print(move, file=sys.stderr)
        print(cost, file=sys.stderr)
        action = {'move': move}
        action_json = json.dumps(action)
        print(action_json, file=sys.stderr)
        print(action_json, flush=True)
if __name__ == '__main__':
    main()
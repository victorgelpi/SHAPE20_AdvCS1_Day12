#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
COMS W4701 Artificial Intelligence - Programming Homework 2

An AI player for Othello. This is the template file that you need to  
complete and submit. 

@author: YOUR NAME AND UNI 
"""

import math
import random
import sys
import time

# You can use the functions in othello_shared to write your AI 
from othello_shared import find_lines, get_possible_moves, get_score, play_move

def compute_utility(board, color):
  p1, p2 = get_score(board)
  return p1 - p2


############ MINIMAX ###############################

def minimax_min_node(board, color):
  """
  Evaluates min node and returns a utility.
  """
  opp_color = 1 if color == 2 else 2

  
  #want this to be INF 
  minUtil = math.inf
  #change to color
  moves = get_possible_moves(board, color)

  if not moves:
    return compute_utility(board, color)

  for move in get_possible_moves(board, opp_color):
    i,j = move
    #we want color for play move
    newBoard = play_move(board, color, i,j)
    #use oppsite color
    util = minimax_max_node(newBoard, opp_color)
    minUtil = min(minUtil, util)

  return minUtil


def minimax_max_node(board, color):
  """
  Evaluate max node and return utility. 
  """
  opp_color = 1 if color == 2 else 2

  #want this to be -INF:
  maxUtil = -math.inf
  moves = get_possible_moves(board, color)

  if not moves:
    return compute_utility(board, color)

  for move in moves:
    i,j = move
    newBoard = play_move(board, color, i,j)
    util = minimax_min_node(newBoard, opp_color)
    maxUtil = max(maxUtil, util)

  return maxUtil 

    
def select_move_minimax(board, color):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  
    """
    bestMove = (None, None)
    bestUtil = -math.inf
    opp_color = 1 if color == 2 else 2
    
    #starting is max 
    for move in get_possible_moves(board, color):
       i,j = move
       new_board = play_move(board, color, i,j)
       utility = minimax_min_node(new_board, opp_color)

       if utility > bestUtil:
         bestMove = move

       # select the move that gives the highest utility

    return bestMove # returns a move, NOT the best utility.  
    
############ ALPHA-BETA PRUNING #####################

def alphabeta_min_node(board, color, alpha, level, limit):

  level += 1 #<-----
  if level >= limit: 
    return heuristic_evaluation(board, color)

  opp_color = 1 if color == 2 else 2

  #want this to be -INF:
  moves = get_possible_moves(board, color)

  if not moves:
    return compute_utility(board, color)

  beta = math.inf
  for move in moves:
    i,j = move
    newBoard = play_move(board, color, i,j)
    util = alphabeta_max_node(newBoard, opp_color, beta, level, limit)
    if util <= alpha:
      return util
    beta = min(beta, util)

  return beta 


def alphabeta_max_node(board, color, beta, level, limit):
  
  level += 1 #<-----
  if level >= limit: 
    return heuristic_evaluation(board, color)

  opp_color = 1 if color == 2 else 2

  #want this to be -INF:
  moves = get_possible_moves(board, color)

  if not moves:
    return compute_utility(board, color)

  alpha = -math.inf
  for move in moves:
    i,j = move
    newBoard = play_move(board, color, i,j)
    util = alphabeta_min_node(newBoard, opp_color, alpha, level, limit)
    if util >= beta:
      return util
    alpha = max(alpha, util)

  return alpha

def heuristic_evaluation(board, color):

  p1, p2 = get_score(board)

  #Checking the corners and assigning a higher value to them
  if board[0][0] == 2 or board[0][7] == 2 or board[7][0] == 2 or board[7][7] == 2:
    p1 += 5
  elif board[0][0] == 1 or board[0][7] == 1 or board[7][0] == 1 or board[7][7] == 1:
    p2 += 5

  return p1 - p2


def select_move_alphabeta(board, color): 

  alpha = -math.inf
  beta = math.inf
  bestMove = (None, None)
  bestUtil = -math.inf
  opp_color = 1 if color == 2 else 2
  limit = 6
  level = 1
    
  #starting is max 
  for move in get_possible_moves(board, color):
    i,j = move
    new_board = play_move(board, color, i,j)
    utility = alphabeta_min_node(new_board, opp_color, alpha, level, limit)
    if utility > bestUtil:
      bestMove = move

       # select the move that gives the highest utility

  return bestMove


####################################################
def run_ai():
    """
    This function establishes communication with the game manager. 
    It first introduces itself and receives its color. 
    Then it repeatedly receives the current score and current board state
    until the game is over. 
    """
    print("Minimax AI") # First line is the name of this AI  
    color = int(input()) # Then we read the color: 1 for dark (goes first), 
                         # 2 for light. 

    while True: # This is the main loop 
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input() 
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over. 
            print 
        else: 
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The 
                                  # squares in each row are represented by 
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)
                    
            # Select the move and send it to the manager 
            #movei, movej = select_move_minimax(board, color)
            movei, movej = select_move_alphabeta(board, color)
            print("{} {}".format(movei, movej)) 


if __name__ == "__main__":
    run_ai()
#
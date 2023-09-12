# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing
import math
import time
import sys


random_seed = None


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
  print("INFO")

  return {
    "apiversion": "1",
    "author": "snake2",  # TODO: Your Battlesnake Username
    "color": "#000088",  # TODO: Choose color
    "head": "default",  # TODO: Choose head
    "tail": "default",  # TODO: Choose tail
  }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
  if random_seed is not None:
    random.seed(random_seed)
  print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
  print("GAME OVER\n")


def get_next(current_head, next_move):
  """
    return the coordinate of the head if our snake goes that way
    """
  MOVE_LOOKUP = {"left": -1, "right": 1, "up": 1, "down": -1}
  # Copy first
  future_head = current_head.copy()

  if next_move in ["left", "right"]:
    # X-axis
    future_head["x"] = current_head["x"] + MOVE_LOOKUP[next_move]
  elif next_move in ["up", "down"]:
    future_head["y"] = current_head["y"] + MOVE_LOOKUP[next_move]

  return future_head


def avoid_walls(future_head, board_width, board_height):
  result = True

  x = int(future_head["x"])
  y = int(future_head["y"])

  if x < 0 or y < 0 or x >= board_width or y >= board_height:
    result = False

  return result


def avoid_snakes(future_head, snake_bodies):
  for snake in snake_bodies:
    if future_head in snake["body"][:-1]:
      return False
  return True


# adapted from https://github.com/altersaddle/untimely-neglected-wearable
def get_safe_moves(possible_moves, body, board):
  safe_moves = []
  for guess in possible_moves:
    guess_coord = get_next(body[0], guess)
    if avoid_walls(guess_coord,
                   board["width"], board["height"]) and avoid_snakes(
                     guess_coord, board["snakes"]):
      safe_moves.append(guess)
    elif len(
        body) > 1 and guess_coord == body[-1] and guess_coord not in body[:-1]:
      # The tail is also a safe place to go... unless there is a non-tail segment there too
      safe_moves.append(guess)
  return safe_moves


def fruit_move(safe_moves, body, food):
  move_for_fruit = []
  base_dist = math.dist(
    [int(body[0]["x"]), int(body[0]["y"])],
    [int(food[0]["x"]), int(food[0]["y"])])
  shortest_dist = base_dist
  closest_fruit = food[0]
  if not closest_fruit:
    return move_for_fruit
  for fruit in food:
    local_dist = math.dist(
      [int(body[0]["x"]), int(body[0]["y"])],
      [int(fruit["x"]), int(fruit["y"])])
    if (local_dist < shortest_dist):
      shortest_dist = local_dist
      closest_fruit = fruit
  for move in safe_moves:
    if (math.dist(
      [int(get_next(body[0], move)["x"]),
       int(get_next(body[0], move)["y"])],
      [int(closest_fruit["x"]),
       int(closest_fruit["y"])]) <
        math.dist([int(body[0]["x"]), int(body[0]["y"])],
                  [int(closest_fruit["x"]),
                   int(closest_fruit["y"])])):
      move_for_fruit.append(move)
  return move_for_fruit


def flood_fill(fruit, blocked, board):
  #Creates a empty stack, checked array, and append fruit to stack
  q = []
  q.append(fruit)
  checked = []
  while q:
    #Gets the first element of the stack
    first_element = q.pop()
    #Checks to see if element is in blocked or already been checked (blocked or checked will not execute)
    if first_element not in blocked and first_element not in checked:
      #first_element['x']
      x = first_element[0]
      y = first_element[1]

      checked.append(first_element)
      #print (blocked)

      #Append the four directions of the next location
      if x < board["width"] and x > -1 and y < board["height"] and y > -1:
        new_position = [x + 1, y]
        if new_position not in checked and new_position not in blocked:
          q.append(new_position)

      if x < board["width"] and x > -1 and y < board["height"] and y > -1:
        new_position = [x - 1, y]
        if new_position not in checked and new_position not in blocked:
          q.append(new_position)

      if x < board["width"] and x > -1 and y < board["height"] and y > -1:
        new_position = [x, y + 1]
        if new_position not in checked and new_position not in blocked:
          q.append(new_position)

      if x < board["width"] and x > -1 and y < board["height"] and y > -1:
        new_position = [x, y - 1]
        if new_position not in checked and new_position not in blocked:
          q.append(new_position)

  #returns the size of the amount of open avaliable spaces on the game board. xx--xx
  print(len(checked))
  #print(checked)
  return len(checked)


def closed_in(body, board, safe_moves):
  output = []
  dict = {}
  blocked = []
  spaces = []
  #Gets the snake bodies on the board and append it to blocked
  for b in board["snakes"]:
    for c in b["body"]:
      coord = [c['x'], c['y']]
      blocked.append(coord)
  #Gets the amount of open spaces depending on the direction of the fruit
  for f in safe_moves:
    #Gets the future head of the direction in safe moves
    future_head = get_next(body[0], f)
    f = [future_head['x'], future_head['y']]
    #Calls Flood fill to determine the amount of free spaces near the head
    space = flood_fill(f, blocked, board)
    spaces.append(space)
    #print(spaces)
  #Checks to see if there is no input for the safe moves, if not return
  if (len(spaces) == 0):
    return
  #choose the highest amount of avaliable spaces from the three directions
  highest_move = max(spaces)
  #Turns the three directions into a dictionary with the amount of free spaces.
  for f in safe_moves:
    i = safe_moves.index(f)
    dict[f] = spaces[i]
  #print(dict)

  #Get the move with the highest amount of free spaces
  move = safe_moves[spaces.index(highest_move)]
  #returns a list with the move with the highest amount of free spaces and the dictionary values of each future move
  output = [move, dict]
  return output


def closest_fruit(head, food):
  base_dist = math.dist(
    [int(head["x"]), int(head["y"])],
    [int(food[0]["x"]), int(food[0]["y"])])
  shortest_dist = base_dist
  closest_fruit = food[0]
  for fruit in food:
    local_dist = math.dist([int(head["x"]), int(head["y"])],
                           [int(fruit["x"]), int(fruit["y"])])
    if (local_dist < shortest_dist):
      shortest_dist = local_dist
      closest_fruit = fruit
  return closest_fruit


def closer_to_closestfruit(snakes, game_state):
  try:
    if game_state["you"]["id"] == snakes[1]["id"]:
      opponent_body = snakes[0]["body"]
      self_body = snakes[1]["body"]
    else:
      opponent_body = snakes[1]["body"]
      self_body = snakes[0]["body"]
    closest_fruited = closest_fruit(self_body[0], game_state["board"]["food"])

    my_dist = math.dist([self_body[0]["x"], self_body[0]["y"]],
                        [int(closest_fruited["x"]),
                         int(closest_fruited["y"])])

    enemy_dist = math.dist(
      [opponent_body[0]["x"], opponent_body[0]["y"]],
      [int(closest_fruited["x"]),
       int(closest_fruited["y"])])
    difference = (enemy_dist - my_dist)
    print(difference)
    return difference * 2
  except:
    return 0


def snake_size(body):
  return len(body)


def snake_size_comparaison(game_state):
  try:
    if game_state["you"]["body"] == game_state["board"]["snakes"][1]["body"]:
      opponent_body = game_state["board"]["snakes"][0]["body"]
    else:
      opponent_body = game_state["board"]["snakes"][1]["body"]
    self_body = game_state["you"]["body"]
    difference = (len(self_body) - 1 - len(opponent_body))
    return difference * 4
  except:
    return 0

def numSafeMoves(gameState):
  body = gameState["you"]["body"]
  possible_moves = ["up", "down", "left", "right"]
  move_options = get_safe_moves(possible_moves, body, gameState["board"])
  return len(move_options)




#--------------------------------------------------------------------------Heuristic function
def heuristic(gameState, snakes):
  h = 0
  h += snake_size_comparaison(gameState)
  print(snake_size_comparaison(gameState))
  h += closer_to_closestfruit(snakes, gameState)
  print(closer_to_closestfruit(snakes, gameState))
  h += numSafeMoves(gameState)
  
  return h


def createNewState(gameState, snakes, move, me):
  tempState = snakes
  i = 0
  for snake in tempState:
    if me:
      if gameState["you"]["id"] == snake["id"]:
        tempState[i]["body"][0] = get_next(tempState[i]["body"][0], move)
        i = i + 1
    else:
      if gameState["you"]["id"] is not snake["id"]:
        tempState[i]["body"][0] = get_next(tempState[i]["body"][0], move)
        i = i + 1
  return tempState


#==================== minimax function ==================================
def minimax(gameState, snakes, depth, maximizingPlayer):
  body = gameState["you"]["body"]
  possible_moves = ["up", "down", "left", "right"]
  move_options = get_safe_moves(possible_moves, body, gameState["board"])
  if depth == 0 or end(gameState):
    return heuristic(gameState, snakes)
  if maximizingPlayer:
    value = -sys.maxsize - 1
    bestMove = None
    for moves in move_options:
      newState = createNewState(gameState, snakes, moves, True)
      store = minimax(gameState, newState, depth - 1, False)
      if (value < store[0]):
        value = store[0]
        bestMove = moves
    return (value, bestMove)
  else:  # minimizing player
    value = sys.maxsize
    bestMove = None
    nodes = {
      'up': createNewState(gameState, snakes, "up", False),
      "down": createNewState(gameState, snakes, "down", False),
      "left": createNewState(gameState, snakes, "left", False),
      "right": createNewState(gameState, snakes, "right", False),
    }
    for child in nodes:
      newState = nodes[child]
      #value, bestMove = min(value, minimax(newState, depth - 1, True))
      store = minimax(gameState, newState, depth - 1, True)
      if (value > store):
        value = store
        bestMove = child
    return (value, bestMove)


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
  next_move = minimax(game_state, game_state['board']['snakes'], 2, True)[1]
  print(f"MOVE {game_state['turn']}: {next_move}")
  return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
  from server import run_server

  port = "8000"
  for i in range(len(sys.argv) - 1):
    if sys.argv[i] == '--port':
      port = sys.argv[i + 1]
    elif sys.argv[i] == '--seed':
      random_seed = int(sys.argv[i + 1])
  run_server({
    "info": info,
    "start": start,
    "move": move,
    "end": end,
    "port": port
  })

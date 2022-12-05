#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
You have just been hired at a video game software house and you have
to render the snake game on an image  by saving the final image of the
snake's path and returning the length of the snake.
Implement the generate_snake function that takes as input a path to an
image file, which is the starting image "start_img". The image can
contain black background pixels, obstacle for the snake as red pixels
and finally food as orange pixels. The snake must be drawn in green.
In addition you must draw in gray the trail that the snake leaves onto
its path. The function also takes as input the initial snake position,
"position" as a list of two integers X and Y. The commands of the
player on how to move the snake in the video game are available in a
string "commands."  The function must save the final image of the
snake's path to the path "out_img," which is passed as the last input
argument to the function. In addition, the function must return the
length of the snake at the end of the game.

Each command in "commands" corresponds to a cardinal sign, followed by
a space. The possible cardinal signs are:

| NW | N | NE |
| W  |   |  E |
| SW | S | SE |

corresponding to one-pixel snake movements such as:

| up-left     | up     | up-right     |
| left        |        | right        |
| bottom-left | bottom | bottom-right |

The snake moves according to the commands; in the case the snake
eats food, it increases its size by one pixel.

The snake can move from side to side of the image, horizontally and
vertically, this means that if the snake crosses a side of the image,
it will appear again from the opposite side.
The game ends when the commands are over or the snake dies. The snake
dies when:
- it hits an obstacle
- it hits itself so it cannot pass over itself
- crosses itself diagonally. As an examples, a 1->2->3-4 path like the
  one below on the left is not allowed; while the one on the right is
  OK.

  NOT OK - diagonal cross        OK - not a diagonal cross
       | 4 | 2 |                    | 1 | 2 |
       | 1 | 3 |                    | 4 | 3 |

For example, considering the test case data/input_00.json
the snake starts from "position": [12, 13] and receives the commands
 "commands": "S W S W W S W N N W N N N N N W N" 
generates the image in visible in data/expected_end_00.png
and returns 5 since the snake is 5 pixels long at the
end of the game.

NOTE: Analyze the images to get the exact color values to use.

NOTE: do not import or use any other library except images.
'''


import images as imgs

def pos_on_map_simple(x, y, move, game_map):
  length, width = len(game_map), len(game_map[0])
  if move == "N":
    if x <= 0:
      return [game_map[length-1][y], length-1, y]
    else:
      return [game_map[x-1][y], x-1, y]
  
  if move == "W":
    if y <= 0:
      return [game_map[x][width-1], x, width-1]
    else:
      return [game_map[x][y-1], x, y-1]

  if move == "E":
    if y == width-1:
      return [game_map[x][0], x, 0]
    else:
      return [game_map[x][y+1], x, y+1]

  if move == "S":
    if x >= length-1:
      return [game_map[0][y], 0, y]
    else:
      return [game_map[x+1][y], x+1, y]

def pos_on_map_diagonally(x, y, move, game_map):
  x, y = pos_on_map_simple(x, y, move[0], game_map)[1], pos_on_map_simple(x, y, move[0], game_map)[2]
  return pos_on_map_simple(x, y, move[1], game_map)


def pos_on_map(x, y, move, game_map):
  if len(move) == 1:
    return pos_on_map_simple(x, y, move, game_map)
  else:
    return pos_on_map_diagonally(x, y, move, game_map)

def is_suicide(x, y, move, game_map):
  dest, destX, destY = pos_on_map(x, y, move, game_map)
  if dest == (0, 255, 0):
    # simple
    return True
  if move in ["NE","NW","SE","SW"]:
    # crossover
    vertical = game_map[destX][y]
    horizental = game_map[x][destY]
    return vertical == (0, 255, 0) and horizental == (0, 255, 0)
  return False


def is_obstacle(x, y, move, game_map):
  if pos_on_map(x, y, move, game_map)[0] == (255, 0, 0):
    return True 
  return False


def game_finished(x, y, move, game_map):
  return is_suicide(x, y, move, game_map) or is_obstacle(x, y, move, game_map)


def eat_orange(x, y, move, game_map):
  if pos_on_map(x, y, move, game_map)[0]==(255, 128, 0):
    return True
  return False


def generate_snake(start_img: str, position: list[int, int],
                   commands: str, out_img: str) -> int:
    # Write your code here
    snake = []
    
    y, x = position
    size = 1
    game_map = imgs.load(start_img)
    game_map[x][y]=(0, 255, 0)
    snake.append((x,y))
    i=0
    for move in commands.split(' '):
      if game_finished(x, y, move, game_map):
        # game_map[x][y] = (0, 255, 0)
        imgs.save(game_map, out_img)
        return len(snake)
      if eat_orange(x, y, move, game_map):
        size += 1
        x, y = pos_on_map(x, y, move, game_map)[1:]
        snake.append((x,y))
        game_map[x][y] = (0, 255, 0)
      else:
        x, y = pos_on_map(x, y, move, game_map)[1:]
        snake.append((x, y))
        game_map[x][y] = (0, 255, 0)
        x_tail, y_tail = snake.pop(0)
        game_map[x_tail][y_tail] = (128, 128, 128)
    imgs.save(game_map, out_img)
    return size

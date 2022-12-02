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

def pos_on_map(x, y, move, game_map):
  width, length = len(game_map), len(game_map[0])
  if move == "N":
    if y-1 < 0:
      return game_map[x][length-1], x, length-1
    else:
      return [game_map[x][y-1], x, y-1]
  
  if move == "W":
    if x-1 < 0:
      return game_map[width-1][y], width-1, y
    else:
      return [game_map[x][y-1], x, y-1]

  if move == "E":
    if x == width-1:
      return [game_map[0][y], 0, y]
    else:
      return [game_map[x+1][y], x+1, y]

  if move == "S":
    if y == length-1:
      return [game_map[x][0], x, 0]
    else:
      return [game_map[x][y+1], x, y+1]

  if move == "SW":
    if x==0 and y==length-1:
      return [game_map[width-1][0], width-1, 0]
    elif x==0:
      return [game_map[width-1][y-1], width-1, y-1]
    elif y==width-1:
      return [game_map[x-1][0], x-1, 0]
    else:
      return [game_map[x-1][y+1], x-1, y+1]

  if move == "NE":
    if x==width-1 and y==0:
      return [game_map[0][length-1], 0, length-1]
    elif y==0:
      return [game_map[x+1][length-1], width-1, y-1]
    elif x==width-1:
      return [game_map[0][y+1], 0, y+1]
    else:
      return [game_map[x+1][y-1], x+1, y-1]
  if move == "NW":
    if x==0 and y==0:
      return [game_map[width-1][length-1], width-1, length-1]
    elif y==0:
      return [game_map[x-1][length-1], x-1, length-1]
    elif x==0:
      return [game_map[0][y-1], 0, y-1]
    else:
      return [game_map[x-1][y-1], x-1, y-1]

  if move == "SE":
    if x==width-1 and y==length-1:
      return [game_map[0][0], 0, 0]
    elif x==width-1:
      return [game_map[0][y-1], 0, y-1]
    elif y==length-1:
      return [game_map[x+1][0], x+1, 0]
    else:
      return [game_map[x+1][y+1], x+1, y+1]

def is_suicide(x, y, move, game_map):
  if pos_on_map(x, y, move, game_map)[0]==(0, 255, 0):
    return True
  return False

def is_obstacle(x, y, move, game_map):
  if pos_on_map(x, y, move, game_map)[0] == (255, 0, 0):
    return True 
  return False

def game_finished(x, y, move, game_map):
  if is_suicide(x, y, move, game_map) or is_obstacle(x, y, move, game_map):
    return True
  return False

def eat_orange(x, y, move, game_map):
  if pos_on_map(x, y, move, game_map)[0]==(255, 128, 0):
    return True
  return False


def generate_snake(start_img: str, position: list[int, int],
                   commands: str,) -> int:
    # Write your code here
    snake = []
    out_img=''
    x_head, y_head = position
    x_tail, y_tail = position
    size = 1
    game_map = imgs.load(start_img)
    x, y = position
    game_map[x][y]=(0, 255, 0)
    snake.append((x,y))

    moves_len = len(commands.split(' '))
    i=0
    for move in commands.split(' '):
      if game_finished(x, y, move, game_map):
        game_map[x][y]=(0, 255, 0)
        out_img = imgs.save(game_map)
        return size
      if eat_orange(x, y, move, game_map):
        size += 1
        x, y = pos_on_map(x, y, move, game_map)[1], pos_on_map(x, y, move, game_map)[2]
        game_map[x][y] = (0, 255, 0)
        x_head, y_head = x, y
      else:
        x, y = pos_on_map(x, y, move, game_map)[1], pos_on_map(x, y, move, game_map)[2]
        snake.insert(0,(x, y))
        game_map[snake[-1][0]][snake[-1][1]] = (128, 128, 128)
        del snake[-1]
        x_tail, y_tail = snake[-1]
    print(game_map)
    return size

data= {"input": {"start_img": "./data/input_00.png", "position": [12, 13], "commands": "S W S W W W S W W N N W N N N N N W N", "out_img": "./output/output_end_00.png"}, "expected": ["./data/expected_end_00.png", 5]}

print(generate_snake("data/input_00.png", data["input"]["position"], data["input"]["commands"]))








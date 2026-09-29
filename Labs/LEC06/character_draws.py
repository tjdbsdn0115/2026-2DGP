import math
from pico2d import *

open_canvas(800, 600)
character = load_image('character.png')

def move_circle():
    print('circle')
    for degree in range(0, 91, 5):
        theta = math.radians(degree)
        x = 400 + 200 * math.cos(theta)
        y = 300 + 200 * math.sin(theta)
        clear_canvas()
        character.draw(x, y)
        update_canvas()
        delay(0.1)

def move_rectangle():
    print('rectangle')

def move_triangle():
    print('triangle')

while True:
    move_circle()
    move_rectangle()
    move_triangle()
    break

close_canvas()
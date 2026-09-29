import math
from pico2d import *

open_canvas(800, 600)
character = load_image('character.png')

def move_circle():
    print('circle')
    theta = math.radians(0)
    x = 400 + 200 * math.cos(theta)
    y = 300 + 200 * math.sin(theta)
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(5)

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
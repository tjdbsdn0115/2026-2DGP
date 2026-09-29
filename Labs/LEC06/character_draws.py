import math
from pico2d import *

open_canvas(800, 600)
character = load_image('character.png')

LEFT, RIGHT = 50, 750
BOTTOM, TOP = 50, 550

def draw_character(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(0.01)

def move_circle():
    print('circle')
    for degree in range(360):
        theta = math.radians(degree)
        x = 400 + 200 * math.cos(theta)
        y = 300 + 200 * math.sin(theta)
        draw_character(x, y)
        clear_canvas()
        character.draw(x, y)
        update_canvas()
        delay(0.1)

def move_top():
    for x in range(LEFT, RIGHT + 1, 5):
        draw_character(x, TOP)

def move_right():
    for y in range(TOP - 5, BOTTOM - 1, -5):
        draw_character(RIGHT, y)

def move_bottom():
    for x in range(RIGHT - 5, LEFT - 1, -5):
        draw_character(x, BOTTOM)

def move_left():
    for y in range(BOTTOM + 5, TOP + 1, 5):
        draw_character(LEFT, y)

def move_rectangle():
    print('rectangle')
    move_top()
    move_right()
    move_bottom()
    move_left() 

def move_ab():
    for x in range(100, 701, 5):
        draw_character(x, 100)

def move_bc():
    print('B -> C')

def move_ca():
    print('C -> A')

def move_triangle():
    print('triangle')
    move_ab()
    move_bc()
    move_ca()

while True:
    move_circle()
    move_rectangle()
    move_triangle()
    break

close_canvas()
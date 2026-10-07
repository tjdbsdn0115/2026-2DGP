import math
from pico2d import *


FRAME_DELAY = 0.001
CENTER = (400, 300)
RADIUS = 200

LEFT, RIGHT = 50, 750
BOTTOM, TOP = 50, 550
A, B, C = (100, 100), (700, 100), (400, 500)


def draw_character(character, x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(FRAME_DELAY)


def move_segment(character, start, end, steps):
    x0, y0 = start
    x1, y1 = end
    for step in range(1, steps + 1):
        t = step / steps
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t
        draw_character(character, x, y)


def move_circle(character):
    for degree in range(0, 360, 2):
        angle = math.radians(degree)
        x = CENTER[0] + RADIUS * math.cos(angle)
        y = CENTER[1] + RADIUS * math.sin(angle)
        draw_character(character, x, y)


def move_rectangle(character):
    corners = [
        (LEFT, TOP),
        (RIGHT, TOP),
        (RIGHT, BOTTOM),
        (LEFT, BOTTOM),
        (LEFT, TOP),
    ]
    draw_character(character, *corners[0])
    for start, end, steps in zip(corners, corners[1:], (140, 100, 140, 100)):
        move_segment(character, start, end, steps)


def move_triangle(character):
    corners = (A, B, C, A)
    draw_character(character, *A)
    for start, end in zip(corners, corners[1:]):
        move_segment(character, start, end, 100)


def main():
    open_canvas(800, 600)
    try:
        character = load_image('character.png')
        while True:
            move_circle(character)
            move_rectangle(character)
            move_triangle(character)
    except KeyboardInterrupt:
        pass
    finally:
        close_canvas()


if __name__ == '__main__':
    main()

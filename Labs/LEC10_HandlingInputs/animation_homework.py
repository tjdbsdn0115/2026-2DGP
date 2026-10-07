from pico2d import *
from pathlib import Path

WIDTH, HEIGHT = 1000, 800
FRAME_SIZE = 100
ASSET_DIR = Path(__file__).resolve().parent

running = True
x, y = WIDTH / 2, HEIGHT / 2
frame = 0
pressed_keys = set()
ARROW_KEYS = {SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN}


def handle_events():
    global running
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key in ARROW_KEYS:
                pressed_keys.add(event.key)
        elif event.type == SDL_KEYUP:
            pressed_keys.discard(event.key)


def update():
    global x, y
    dx = int(SDLK_RIGHT in pressed_keys) - int(SDLK_LEFT in pressed_keys)
    dy = int(SDLK_UP in pressed_keys) - int(SDLK_DOWN in pressed_keys)
    x += dx * 3
    y += dy * 3


def draw(background, character):
    clear_canvas()
    background.draw(WIDTH / 2, HEIGHT / 2, WIDTH, HEIGHT)
    character.clip_draw(frame * FRAME_SIZE, 300, FRAME_SIZE, FRAME_SIZE, x, y)
    update_canvas()


def main():
    open_canvas(WIDTH, HEIGHT)
    try:
        background = load_image(str(ASSET_DIR / 'TUK_GROUND.png'))
        character = load_image(str(ASSET_DIR / 'animation_sheet.png'))
        while running:
            handle_events()
            if not running:
                break
            update()
            draw(background, character)
            delay(0.01)
    finally:
        close_canvas()


if __name__ == '__main__':
    main()

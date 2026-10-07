from pico2d import *
from pathlib import Path
from time import perf_counter
from math import hypot

WIDTH, HEIGHT = 1000, 800
FRAME_SIZE = 100
MOVE_SPEED = 250.0
ANIMATION_FPS = 10.0
FRAME_COUNT = 8
ASSET_DIR = Path(__file__).resolve().parent

running = True
x, y = WIDTH / 2, HEIGHT / 2
frame = 0
facing = 'RIGHT'
state = 'IDLE'
animation_time = 0.0
animation = ('IDLE', 'RIGHT')
pressed_keys = set()
ARROW_KEYS = {SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN}


def handle_events():
    global running, facing
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key in ARROW_KEYS:
                pressed_keys.add(event.key)
                if event.key == SDLK_LEFT:
                    facing = 'LEFT'
                elif event.key == SDLK_RIGHT:
                    facing = 'RIGHT'
        elif event.type == SDL_KEYUP:
            pressed_keys.discard(event.key)
    if not SDL_GetKeyboardFocus():
        pressed_keys.clear()


def update(dt):
    global x, y, frame, state, animation_time, animation
    dx = int(SDLK_RIGHT in pressed_keys) - int(SDLK_LEFT in pressed_keys)
    dy = int(SDLK_UP in pressed_keys) - int(SDLK_DOWN in pressed_keys)
    length = hypot(dx, dy)
    if length:
        dx, dy = dx / length, dy / length
    old_x, old_y = x, y
    half = FRAME_SIZE / 2
    x = max(half, min(WIDTH - half, x + dx * MOVE_SPEED * dt))
    y = max(half, min(HEIGHT - half, y + dy * MOVE_SPEED * dt))
    state = 'MOVE' if (x, y) != (old_x, old_y) else 'IDLE'
    next_animation = (state, facing)
    if next_animation != animation:
        animation_time = 0.0
        animation = next_animation
    animation_time += dt
    frame = int(animation_time * ANIMATION_FPS) % FRAME_COUNT


def draw(background, character):
    clear_canvas()
    background.draw(WIDTH / 2, HEIGHT / 2, WIDTH, HEIGHT)
    # 시트 아래부터: 왼쪽 이동, 오른쪽 이동, 왼쪽 대기, 오른쪽 대기.
    row = (2 if state == 'IDLE' else 0) + (1 if facing == 'RIGHT' else 0)
    character.clip_draw(frame * FRAME_SIZE, row * FRAME_SIZE,
                        FRAME_SIZE, FRAME_SIZE, x, y)
    update_canvas()


def main():
    open_canvas(WIDTH, HEIGHT)
    try:
        background = load_image(str(ASSET_DIR / 'TUK_GROUND.png'))
        character = load_image(str(ASSET_DIR / 'animation_sheet.png'))
        previous_time = perf_counter()
        while running:
            now = perf_counter()
            dt = min(now - previous_time, 0.05)
            previous_time = now
            handle_events()
            if not running:
                break
            update(dt)
            draw(background, character)
            delay(0.01)
    finally:
        close_canvas()


if __name__ == '__main__':
    main()

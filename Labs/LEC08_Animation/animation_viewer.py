# Drill #8: LEC08 방식으로 새로 제작한 캐릭터 이미지 재생
from pico2d import *
from time import perf_counter
from pathlib import Path

WIDTH, HEIGHT = 960, 720
SCALE = 3  # 가장 작은 자세도 화면 높이의 절반 이상으로 표시
REPEAT_COUNT = 5
PAUSE_SECONDS = 1.0


# 새 PNG에서 직접 확인한 프레임: (왼쪽 x, 위쪽 y, 폭, 높이)
# 대기 4개 / 걷기 8개 / 점프 6개 / 공격 6개
animations = [
    ("Idle", 6, [
        (47, 69, 137, 174), (236, 69, 137, 174), (424, 69, 136, 174),
        (616, 69, 137, 174),
    ]),
    ("Walk", 10, [
        (36, 306, 162, 179), (230, 306, 156, 179), (417, 306, 158, 180),
        (606, 304, 156, 182), (792, 310, 157, 175), (981, 303, 160, 183),
        (1170, 303, 157, 182), (1356, 304, 155, 181),
    ]),
    ("Jump", 8, [
        (37, 604, 166, 135), (230, 566, 144, 179), (422, 542, 168, 169),
        (596, 526, 166, 157), (791, 563, 170, 160), (985, 599, 161, 140),
    ]),
    ("Attack", 10, [
        (40, 807, 162, 169), (216, 809, 155, 167), (423, 751, 142, 225),
        (593, 815, 216, 161), (789, 810, 206, 166), (1001, 806, 161, 170),
    ]),
]


def draw_frame(sheet, frame):
    left, top, width, height = frame
    bottom = sheet.h - top - height  # pico2d는 아래쪽이 y=0
    sheet.clip_draw(left, bottom, width, height, WIDTH / 2, HEIGHT / 2,
                    width * SCALE, height * SCALE)


def show_for(sheet, frame, seconds):
    clear_canvas()
    draw_frame(sheet, frame)
    update_canvas()
    end = perf_counter() + seconds
    while perf_counter() < end:
        for event in get_events():
            if event.type == SDL_QUIT:
                return False
            if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                return False
        delay(min(0.01, max(0, end - perf_counter())))
    return True


def main():
    open_canvas(WIDTH, HEIGHT)
    try:
        image_path = Path(__file__).resolve().parent / "adventurer_sheet.png"
        sheet = load_image(str(image_path))
        while True:
            for name, fps, frames in animations:
                for repeat in range(REPEAT_COUNT):
                    for frame in frames:
                        if not show_for(sheet, frame, 1 / fps):
                            return
                if not show_for(sheet, frames[-1], PAUSE_SECONDS):
                    return
    finally:
        close_canvas()


if __name__ == "__main__":
    main()

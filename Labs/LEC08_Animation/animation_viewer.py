# Drill #8: LEC08의 pico2d 예제를 이용한 애니메이션 뷰어
from pico2d import *
from time import perf_counter
from pathlib import Path

WIDTH, HEIGHT = 960, 720
SCALE = 6  # 가장 짧은 63px 자세도 378px로 표시
REPEAT_COUNT = 5
PAUSE_SECONDS = 1.0
CELL_SIZE = 128
ANCHOR_X, ANCHOR_Y = 69, 85.5  # 원본 128px 칸 안의 공통 중심


# 각 프레임: (왼쪽 x, 위쪽 y, 폭, 높이)
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
    ("Run", 12, [
        (15, 305, 51, 79), (143, 306, 51, 78), (271, 307, 57, 77),
        (399, 306, 51, 78), (527, 305, 51, 79), (655, 306, 51, 78),
        (783, 307, 57, 77), (911, 306, 51, 78),
    ]),
    ("Jump", 12, [
        (15, 432, 60, 80), (141, 435, 62, 76), (269, 438, 65, 74),
        (399, 432, 58, 80), (531, 429, 53, 82), (661, 430, 53, 80),
        (790, 432, 51, 74), (918, 434, 53, 70), (1046, 438, 53, 74),
        (1174, 441, 52, 71), (1302, 442, 51, 70), (1431, 449, 50, 63),
    ]),
    ("Attack", 10, [
        (19, 566, 53, 74), (148, 567, 52, 73), (276, 567, 57, 73),
        (404, 566, 63, 74), (532, 566, 101, 74), (660, 566, 54, 74),
    ]),
]


def draw_frame(sheet, frame):
    left, top, width, height = frame
    bottom = sheet.h - top - height  # pico2d는 아래쪽이 y=0
    # 잘라낸 크기가 달라도 원래 자세의 위치를 보존한다.
    x = WIDTH / 2 + (left % CELL_SIZE + width / 2 - ANCHOR_X) * SCALE
    y = HEIGHT / 2 + (ANCHOR_Y - top % CELL_SIZE - height / 2) * SCALE
    sheet.clip_draw(left, bottom, width, height, x, y,
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
        image_path = Path(__file__).resolve().parent / "SamuraiSheet.png"
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

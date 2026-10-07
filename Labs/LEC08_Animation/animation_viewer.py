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
        (47, 69, 138, 174), (236, 69, 136, 174), (423, 69, 138, 174),
        (616, 69, 137, 174),
    ]),
    ("Walk", 10, [
        (37, 306, 161, 180), (230, 306, 156, 180), (417, 306, 159, 180),
        (606, 305, 156, 180), (792, 310, 157, 176), (981, 303, 160, 183),
        (1171, 303, 156, 183), (1356, 304, 155, 181),
    ]),
    ("Jump", 8, [
        (37, 604, 165, 136), (231, 566, 143, 179), (422, 542, 168, 170),
        (597, 526, 165, 158), (791, 563, 170, 160), (986, 599, 160, 141),
    ]),
    ("Attack", 10, [
        (39, 807, 163, 169), (217, 809, 154, 167), (423, 751, 142, 225),
        (608, 811, 208, 165), (843, 809, 188, 167), (1033, 807, 161, 169),
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

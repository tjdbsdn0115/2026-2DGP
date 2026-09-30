# Drill #8: LEC08의 pico2d 예제를 이용한 애니메이션 뷰어
from pico2d import *
from time import perf_counter

WIDTH, HEIGHT = 960, 720
SCALE = 6
ANCHOR_X, ANCHOR_Y = 69, 85.5  # 원본 128px 칸 안의 공통 중심


# 각 프레임: (왼쪽 x, 위쪽 y, 폭, 높이)
animations = [
    ("Idle", 8, [
        (35, 45, 46, 81), (163, 44, 46, 82), (291, 43, 46, 83),
        (419, 43, 46, 83), (547, 43, 46, 83), (675, 44, 46, 82),
    ]),
    ("Walk", 10, [
        (24, 173, 48, 83), (152, 172, 48, 84), (280, 173, 51, 83),
        (408, 174, 48, 82), (536, 173, 48, 83), (664, 172, 48, 84),
        (792, 173, 52, 83), (920, 174, 48, 82),
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
    x = WIDTH / 2 + (left % 128 + width / 2 - ANCHOR_X) * SCALE
    y = HEIGHT / 2 + (ANCHOR_Y - top % 128 - height / 2) * SCALE
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
    sheet = load_image("SamuraiSheet.png")
    while True:
        for name, fps, frames in animations:
            for repeat in range(5):
                for frame in frames:
                    if not show_for(sheet, frame, 1 / fps):
                        return
            if not show_for(sheet, frames[-1], 1):
                return
    close_canvas()


if __name__ == "__main__":
    main()

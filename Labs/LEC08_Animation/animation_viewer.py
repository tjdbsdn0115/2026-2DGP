# Drill #8: LEC08의 pico2d 예제를 이용한 애니메이션 뷰어
from pico2d import *

WIDTH, HEIGHT = 960, 720
SCALE = 6
ANCHOR_X, ANCHOR_Y = 69, 85.5  # 원본 128px 칸 안의 공통 중심


# 각 프레임: (왼쪽 x, 위쪽 y, 폭, 높이)
frames = [
    (35, 45, 46, 81),
    (163, 44, 46, 82),
    (291, 43, 46, 83),
    (419, 43, 46, 83),
    (547, 43, 46, 83),
    (675, 44, 46, 82),
]


def draw_frame(sheet, frame):
    left, top, width, height = frame
    bottom = sheet.h - top - height  # pico2d는 아래쪽이 y=0
    # 잘라낸 크기가 달라도 원래 자세의 위치를 보존한다.
    x = WIDTH / 2 + (left % 128 + width / 2 - ANCHOR_X) * SCALE
    y = HEIGHT / 2 + (ANCHOR_Y - top % 128 - height / 2) * SCALE
    sheet.clip_draw(left, bottom, width, height, x, y,
                    width * SCALE, height * SCALE)


def main():
    open_canvas(WIDTH, HEIGHT)
    sheet = load_image("SamuraiSheet.png")
    for frame in frames:
        clear_canvas()
        draw_frame(sheet, frame)
        update_canvas()
        delay(0.1)
    close_canvas()


if __name__ == "__main__":
    main()

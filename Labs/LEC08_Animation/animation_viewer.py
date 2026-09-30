# Drill #8: LEC08의 pico2d 예제를 이용한 애니메이션 뷰어
from pico2d import *

SCALE = 6


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
    sheet.clip_draw(left, bottom, width, height, 400, 300,
                    width * SCALE, height * SCALE)


def main():
    open_canvas()
    sheet = load_image("SamuraiSheet.png")
    clear_canvas()
    draw_frame(sheet, frames[0])
    update_canvas()
    delay(0.1)
    close_canvas()


if __name__ == "__main__":
    main()

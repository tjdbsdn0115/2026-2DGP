# Drill #8: LEC08의 pico2d 예제를 이용한 애니메이션 뷰어
from pico2d import *


def main():
    open_canvas()
    sheet = load_image("SamuraiSheet.png")
    clear_canvas()
    update_canvas()
    delay(0.1)
    close_canvas()


if __name__ == "__main__":
    main()

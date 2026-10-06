"""소닉 스프라이트를 동작별로 확대 재생하는 pico2d 뷰어."""

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 600
SCALE = 4
FRAME_INTERVAL = 0.1
REPEAT_COUNT = 5
PAUSE_SECONDS = 1.0


def main():
    """프로그램 진입점."""
    import pico2d

    pico2d.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        pico2d.clear_canvas()
        pico2d.update_canvas()
    finally:
        pico2d.close_canvas()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

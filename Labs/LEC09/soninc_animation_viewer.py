"""소닉 스프라이트를 동작별로 확대 재생하는 pico2d 뷰어."""

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 600
SCALE = 4
FRAME_INTERVAL = 0.1
REPEAT_COUNT = 5
PAUSE_SECONDS = 1.0


def should_quit(events, graphics):
    """창 닫기 또는 ESC를 모든 재생 상태에서 처리한다."""
    return any(
        event.type == graphics.SDL_QUIT
        or (event.type == graphics.SDL_KEYDOWN
            and event.key == graphics.SDLK_ESCAPE)
        for event in events
    )


def main():
    """프로그램 진입점."""
    import pico2d

    pico2d.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        while not should_quit(pico2d.get_events(), pico2d):
            pico2d.clear_canvas()
            pico2d.update_canvas()
            pico2d.delay(0.005)
    finally:
        pico2d.close_canvas()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

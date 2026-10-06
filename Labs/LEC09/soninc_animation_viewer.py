"""소닉 스프라이트를 동작별로 확대 재생하는 pico2d 뷰어."""

from pathlib import Path
from dataclasses import dataclass

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 600
SCALE = 4
FRAME_INTERVAL = 0.1
REPEAT_COUNT = 5
PAUSE_SECONDS = 1.0
SPRITE_PATH = Path(__file__).resolve().with_name("sonic-sprite.png")


@dataclass(frozen=True)
class Frame:
    """위쪽 기준 자르기 영역과 프레임 안의 표시 기준점."""

    left: int
    top: int
    width: int
    height: int
    anchor_x: float
    anchor_y: float

    def bottom(self, image_height):
        return image_height - self.top - self.height

    def validate(self, image_width, image_height):
        if (self.left < 0 or self.top < 0 or self.width <= 0
                or self.height <= 0 or self.left + self.width > image_width
                or self.top + self.height > image_height):
            raise ValueError(f"이미지 범위를 벗어난 프레임: {self}")


FIRST_FRAME = Frame(1, 39, 29, 39, 14.5, 39)


def load_sprite(graphics, path=SPRITE_PATH):
    """실행 파일 위치를 기준으로 이미지를 한 번 읽는다."""
    if not path.is_file():
        raise FileNotFoundError(f"스프라이트 이미지가 없습니다: {path}")
    try:
        return graphics.load_image(str(path))
    except Exception as error:
        raise RuntimeError(f"스프라이트 이미지 읽기 실패: {path} ({error!r})") from error


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
        sprite = load_sprite(pico2d)
        while not should_quit(pico2d.get_events(), pico2d):
            pico2d.clear_canvas()
            pico2d.update_canvas()
            pico2d.delay(0.005)
    finally:
        pico2d.close_canvas()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

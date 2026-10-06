"""소닉 스프라이트를 동작별로 확대 재생하는 pico2d 뷰어."""

from pathlib import Path
from dataclasses import dataclass
from time import monotonic
from math import isfinite
import sys

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 600
SCALE = 4
BASELINE_Y = CANVAS_HEIGHT / 2 - 20 * SCALE
FRAME_INTERVAL = 0.1
REPEAT_COUNT = 5
PAUSE_SECONDS = 1.0
PLAYING = "PLAYING"
PAUSED = "PAUSED"
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


@dataclass(frozen=True)
class Animation:
    name: str
    frames: tuple[Frame, ...]
    interval: float = FRAME_INTERVAL


def frames_from_rectangles(rectangles):
    """행의 공통 발 기준선을 유지해 자르기 높이에 따른 흔들림을 줄인다."""
    baseline = max(top + height for _, top, _, height in rectangles)
    return tuple(Frame(left, top, width, height, width / 2, baseline - top)
                 for left, top, width, height in rectangles)


# 시트의 위쪽 행부터 아래쪽 행, 각 행은 왼쪽부터 오른쪽 순서.
# 첫 행의 3개 경계는 픽셀이 맞닿아 있어 명시적으로 분리한다.
ANIMATIONS = (
    Animation("대기", frames_from_rectangles((
        (1, 39, 29, 39), (31, 40, 26, 38), (58, 39, 29, 39),
        (87, 40, 29, 38), (118, 40, 30, 38), (150, 40, 30, 38),
        (182, 40, 29, 38), (211, 39, 29, 38), (240, 39, 29, 38),
        (270, 45, 24, 32), (302, 51, 29, 26),
    ))),
    Animation("달리기", frames_from_rectangles((
        (8, 80, 26, 37), (37, 80, 27, 37), (65, 80, 31, 38),
        (97, 80, 37, 37), (135, 80, 32, 35), (170, 80, 32, 37),
        (206, 80, 26, 37), (238, 80, 24, 37), (263, 80, 30, 37),
        (295, 80, 36, 37), (334, 80, 32, 36), (370, 80, 29, 37),
    ))),
    Animation("빠른 달리기", frames_from_rectangles((
        (1, 124, 33, 40),
        (39, 124, 35, 39),
        (89, 125, 35, 38),
        (130, 123, 34, 40),
        (181, 123, 34, 40),
        (228, 123, 33, 39),
    ))),
    Animation("회전", frames_from_rectangles((
        (1, 169, 29, 30),
        (35, 168, 29, 30),
        (67, 169, 30, 29),
        (98, 169, 31, 29),
        (131, 168, 29, 30),
        (162, 168, 29, 31),
        (193, 170, 30, 29),
        (230, 170, 31, 29),
        (268, 170, 30, 30),
    ))),
    Animation("회전 공", frames_from_rectangles((
        (1, 206, 30, 27),
        (36, 206, 29, 27),
        (70, 206, 29, 27),
        (105, 206, 29, 27),
        (139, 206, 29, 27),
        (174, 206, 29, 27),
    ))),
    Animation("제자리 회전 달리기", frames_from_rectangles((
        (1, 239, 29, 35),
        (36, 239, 30, 35),
        (74, 239, 31, 35),
        (111, 239, 31, 35),
        (149, 239, 30, 35),
        (186, 239, 31, 35),
    ))),
    Animation("제자리 질주", frames_from_rectangles((
        (1, 283, 29, 35),
        (36, 283, 30, 35),
        (72, 286, 39, 31),
        (123, 285, 39, 32),
        (172, 286, 39, 31),
        (218, 285, 38, 32),
    ))),
    Animation("공중 회전", frames_from_rectangles((
        (1, 328, 24, 42),
        (31, 328, 29, 42),
        (65, 328, 20, 42),
        (90, 328, 25, 42),
        (119, 328, 25, 42),
        (149, 328, 20, 42),
        (184, 341, 40, 28),
        (232, 341, 39, 27),
    ))),
    Animation("걷기", frames_from_rectangles((
        (1, 379, 27, 37),
        (31, 379, 31, 36),
        (64, 379, 31, 36),
        (99, 378, 33, 37),
        (136, 379, 32, 36),
        (176, 379, 33, 36),
        (217, 379, 33, 36),
        (254, 378, 33, 36),
    ))),
    Animation("피격 및 회복", frames_from_rectangles((
        (6, 429, 34, 40),
        (49, 427, 34, 42),
        (96, 427, 23, 39),
        (125, 427, 23, 39),
    ))),
)


def validate_animations(image_width, image_height):
    if not ANIMATIONS:
        raise ValueError("등록된 동작이 없습니다.")
    for animation in ANIMATIONS:
        if not animation.frames or animation.interval <= 0:
            raise ValueError(f"잘못된 동작 데이터: {animation.name}")
        for frame in animation.frames:
            frame.validate(image_width, image_height)


class Player:
    """그리기 빈도와 독립적인 경과 시간 기반 프레임 재생."""

    def __init__(self):
        self.state = PLAYING
        self.animation_index = 0
        self.frame_index = 0
        self.completed_repeats = 0
        self.completed_cycles = 0
        self.elapsed = 0.0

    @property
    def animation(self):
        return ANIMATIONS[self.animation_index]

    @property
    def frame(self):
        return self.animation.frames[self.frame_index]

    def update(self, delta):
        if not isfinite(delta) or delta < 0:
            raise ValueError("경과 시간은 유한한 0 이상의 수여야 합니다.")
        self.elapsed += delta
        while True:
            duration = (self.animation.interval if self.state == PLAYING
                        else PAUSE_SECONDS)
            if self.elapsed + 1e-12 < duration:
                return
            self.elapsed = max(0.0, self.elapsed - duration)
            if self.state == PAUSED:
                self.animation_index = (self.animation_index + 1) % len(ANIMATIONS)
                if self.animation_index == 0:
                    self.completed_cycles += 1
                self.frame_index = 0
                self.completed_repeats = 0
                self.state = PLAYING
                continue
            self.frame_index += 1
            if self.frame_index == len(self.animation.frames):
                self.completed_repeats += 1
                if self.completed_repeats == REPEAT_COUNT:
                    self.frame_index -= 1
                    self.state = PAUSED
                else:
                    self.frame_index = 0


def draw_frame(sprite, frame):
    """프레임 종횡비를 유지하여 화면 중앙에 4배 출력한다."""
    sprite.clip_draw(
        frame.left, frame.bottom(sprite.h), frame.width, frame.height,
        CANVAS_WIDTH / 2 + (frame.width / 2 - frame.anchor_x) * SCALE,
        BASELINE_Y + (frame.anchor_y - frame.height / 2) * SCALE,
        frame.width * SCALE, frame.height * SCALE,
    )


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
    canvas_open = False
    try:
        import pico2d

        try:
            pico2d.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
            canvas_open = True
            pico2d.hide_lattice()
            sprite = load_sprite(pico2d)
            validate_animations(sprite.w, sprite.h)
            player = Player()
            previous = monotonic()
            while not should_quit(pico2d.get_events(), pico2d):
                now = monotonic()
                player.update(now - previous)
                previous = now
                pico2d.clear_canvas()
                draw_frame(sprite, player.frame)
                pico2d.update_canvas()
                pico2d.delay(0.005)
        finally:
            if canvas_open:
                pico2d.close_canvas()
    except ImportError as error:
        print(f"pico2d를 불러올 수 없습니다. python -m pip install pico2d ({error})",
              file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 0
    except Exception as error:
        print(f"소닉 애니메이션 뷰어 오류: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

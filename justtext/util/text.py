from dataclasses import dataclass
from ..constants import *

@dataclass
class TextLayout:
    left_margin: int = 0
    x_pos: int = 0
    y_pos: int = 0
    prev_width: int = 0
    line_gap: int = 10

    def start_if_needed(self, baseline: int) -> None:
        if self.y_pos == 0:
            self.left_margin = self.left_margin or baseline
            self.x_pos = self.left_margin
            self.y_pos = baseline

    def next_line(self, line_height: int) -> None:
        self.y_pos += self.line_gap + line_height
        self.x_pos = self.left_margin
        self.prev_width = 0


class TextRenderer:
    def __init__(self, font):
        self.font = font
        self.layout = TextLayout()

    def reset_layout(self, left_margin: int | None = None) -> None:
        self.layout = TextLayout(left_margin=left_margin or 0)

    def draw(self, surface, text, color=WHITE, bg=0, new_line=True, x_offset=0, y_offset=0, l_offset=0, first_line=False, alignment="none"):
        img = self.font.render(f"{text}", True, color, bg)
        self.layout.start_if_needed(self.font.get_height())

        if new_line:
            if not first_line:
                self.layout.next_line(img.get_height())
        else:
            self.layout.x_pos += self.layout.prev_width + x_offset

        if alignment=="none":
            draw_x = self.layout.x_pos + l_offset
            draw_y = self.layout.y_pos + y_offset
        elif alignment=="middle":
            draw_x = (surface.get_width() / 2) - (img.get_width() / 2)
            draw_y = self.layout.y_pos + y_offset
   
        surface.blit(img, (draw_x, draw_y))
        self.layout.prev_width = img.get_width()

    def addOffset(self, plane: str, offset_amount: int):
        if plane == "x":
            self.layout.x_pos += offset_amount
        elif plane == "y":
            self.layout.y_pos += offset_amount

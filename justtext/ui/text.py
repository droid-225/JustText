from dataclasses import dataclass


@dataclass
class TextLayout:
    left_margin: int = 0
    cursor_x: int = 0
    cursor_y: int = 0
    prev_width: int = 0
    line_gap: int = 10

    def start_if_needed(self, baseline: int) -> None:
        if self.cursor_y == 0:
            self.left_margin = self.left_margin or baseline
            self.cursor_x = self.left_margin
            self.cursor_y = baseline

    def next_line(self, line_height: int) -> None:
        self.cursor_y += self.line_gap + line_height
        self.cursor_x = self.left_margin
        self.prev_width = 0


class TextRenderer:
    def __init__(self, font):
        self.font = font
        self.layout = TextLayout()

    def reset_layout(self, left_margin: int | None = None) -> None:
        self.layout = TextLayout(left_margin=left_margin or 0)

    def draw(self, surface, text, color, bg=0, *, new_line=True, x_offset=0, y_offset=0, l_offset=0, first_line=False):
        img = self.font.render(f"{text}", True, color, bg)
        self.layout.start_if_needed(self.font.get_height())

        if new_line:
            if not first_line:
                self.layout.next_line(img.get_height())
        else:
            self.layout.cursor_x += self.layout.prev_width + x_offset

        draw_x = self.layout.cursor_x + l_offset
        draw_y = self.layout.cursor_y + y_offset
        surface.blit(img, (draw_x, draw_y))
        self.layout.prev_width = img.get_width()



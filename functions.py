import pygame
from random import randint

class Laser:
    def __init__(self, x0, y0, width, height, speed, frame_paths, frame_duration=100):
        """
        ооочень сложный лазер


        :param x0, y0: top-left of rectangle
        :param width, height: dimensions of rectangle perimeter path
        :param speed: pixels per second along perimeter
        :param frame_paths: list of file paths for laser animation frames
        :param frame_duration: ms to display each frame
        """
        # perimeter path
        self.x0, self.y0 = x0, y0
        self.w, self.h = width, height
        self.perim = 2 * (width + height)
        self.pos = 0
        self.speed = speed
        self.angle = 0
        self.x, self.y = x0, y0
        self.last_offset_time = pygame.time.get_ticks()
        self.offset = 0
        # load animation frames
        self.frames = [pygame.image.load(path).convert_alpha() for path in frame_paths]
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.last_frame_time = pygame.time.get_ticks()

    def update(self, dt):
        now = pygame.time.get_ticks()

        if now - self.last_offset_time >= 1500:
            self.offset = randint(10, 90)
            self.last_offset_time = now

        self.pos = (self.pos + self.speed * dt / 1000) % self.perim
        p = self.pos

        if p < self.w:
            self.x = self.x0 + p
            self.y = self.y0 + self.offset
            self.angle = 90
        elif p < self.w + self.h:
            self.x = self.x0 + self.w - self.offset
            self.y = self.y0 + (p - self.w)
            self.angle = 0
        elif p < 2 * self.w + self.h:
            self.x = self.x0 + (self.w - (p - self.w - self.h))
            self.y = self.y0 + self.h - self.offset
            self.angle = 270
        else:
            self.x = self.x0 + self.offset
            self.y = self.y0 + (self.h - (p - 2 * self.w - self.h))
            self.angle = 180

        if now - self.last_frame_time >= self.frame_duration:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_frame_time = now

    def draw(self, surface):
        # get current frame and rotate
        frame = self.frames[self.current_frame]
        rotated = pygame.transform.rotate(frame, self.angle)
        rect = rotated.get_rect(center=(self.x, self.y))
        surface.blit(rotated, rect.topleft)




def render_text_with_outline(text : str, font : pygame.font.Font, text_color : tuple, outline_color: tuple, outline_width=1):
    """
    Рендерит текст с обводкой.

    :param text: str — текст
    :param font: pygame.font.Font — шрифт
    :param text_color: tuple — цвет текста (R, G, B)
    :param outline_color: tuple — цвет обводки (R, G, B)
    :param outline_width: int — толщина обводки (в пикселях)
    :return: pygame.Surface
    """
    base = font.render(text, True, text_color)
    size = (base.get_width() + 2 * outline_width, base.get_height() + 2 * outline_width)
    outline_surface = pygame.Surface(size, pygame.SRCALPHA)

    # Смещения вокруг текста (8 направлений + центр, если хочешь)
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx == 0 and dy == 0:
                continue
            offset_pos = (outline_width + dx, outline_width + dy)
            outline_surface.blit(font.render(text, True, outline_color), offset_pos)

    # Основной текст по центру
    outline_surface.blit(base, (outline_width, outline_width))
    return outline_surface


def render_wrapped_text(sc_w : int, initial_y : int, text : str, font : pygame.font.Font, color : tuple, max_width : int, line_spacing=20, outline_color = None, outline_w=0):
    """
    :param sc_w: int — ширина экрана
    :param initial_y: int — изначальный y текста
    :param text: str — исходный текст
    :param font: pygame.font.Font — шрифт
    :param color: tuple — цвет текста (R, G, B)
    :param max_width: int — максимальная ширина строки
    :param line_spacing: int — вертикальный отступ между строками
    :param outline_color: tuple — цвет подчеркивания
    :param outline_color: int — ширина подчеркивания
    :return: список [surface, [x, y]]
    """
    if outline_color == None:
        outline_color = color

    words = text.split(' ')
    lines = []
    current_line = ''
    
    for word in words:
        test_line = current_line + word + ' '
        test_surface = font.render(test_line, True, color)
        if test_surface.get_width() <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + ' '
    
    if current_line:
        lines.append(current_line.strip())

    surfaces = []
    y_offset = initial_y

    for line in lines:
        surface = render_text_with_outline(line, font, color, outline_color, outline_w)
        surfaces.append([surface, [sc_w / 2 - surface.get_width() / 2, y_offset]])
        y_offset += surface.get_height() + line_spacing

    return surfaces
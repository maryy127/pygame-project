import pygame
from random import randint

class Laser:
    def __init__(self, x0, y0, width, height, speed, frame_paths, laser_shift_sound : pygame.mixer.Sound, frame_duration=100):
        """
        ооочень сложный лазер


        :param x0, y0: top-left of rectangle
        :param width, height: dimensions of rectangle perimeter path
        :param speed: pixels per second along perimeter
        :param frame_paths: list of file paths for laser animation frames
        :param laser_shift_sound: sound of laser's shot
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
        self.laser_sound = laser_shift_sound

        # load animation frames
        self.frames = [pygame.image.load(path).convert_alpha() for path in frame_paths]
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.last_frame_time = pygame.time.get_ticks()

    def update(self, dt):

        now = pygame.time.get_ticks()
        if now - self.last_offset_time >= 1800:
            new_offset = randint(10, 90)
            if abs(new_offset - self.offset) >= 15:  # Воспроизводим звук только если значение увеличилось на значение больщее 9
                self.laser_sound.play()
            self.offset = new_offset
            self.last_offset_time = now

        previous_pos = self.pos
        self.pos = (self.pos + self.speed * dt / 1000) % self.perim
        if self.pos < previous_pos:  
            self.speed = randint(140, 200)
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
        frame = self.frames[self.current_frame]
        rotated = pygame.transform.rotate(frame, self.angle)
        rect = rotated.get_rect(center=(self.x, self.y))
        surface.blit(rotated, rect.topleft)


class Player:
    def __init__(self, ghost_frames, heart_frames, x, y, speed, lives, screen, bounds : list, dead_img):
        self.ghost_frames = [pygame.image.load(f).convert_alpha() for f in ghost_frames]
        self.heart_frames = [pygame.transform.scale(pygame.image.load(f).convert_alpha(), (50, 50)) for f in heart_frames]
        self.x = x; self.y = y; self.speed = speed
        self.lives = lives
        self.screen = screen
        self.current_ghost = 0; self.last_ghost_time = pygame.time.get_ticks()
        self.ghost_slow = 100
        self.width = self.ghost_frames[0].get_width()
        self.height = self.ghost_frames[0].get_height()
        self.bounds = bounds
        self.current_heart = 0
        self.dead = False
        self.death_time = None
        self.dead_img = pygame.image.load(dead_img)
        self.death_s = pygame.mixer.Sound("sfx/player_die.wav")

    def update(self, keys):
        if not self.dead:
            if keys[pygame.K_UP]:    self.y = max(self.bounds[1], self.y - self.speed)
            if keys[pygame.K_DOWN]:  self.y = min(self.bounds[3] - self.height, self.y + self.speed)
            if keys[pygame.K_LEFT]:  self.x = max(self.bounds[0], self.x - self.speed)
            if keys[pygame.K_RIGHT]: self.x = min(self.bounds[2] - self.width, self.x + self.speed)
        
        now = pygame.time.get_ticks()
        if now - self.last_ghost_time >= self.ghost_slow:
            self.current_ghost = (self.current_ghost + 1) % len(self.ghost_frames)
            self.last_ghost_time = now

    def draw(self):
        if not self.dead:
            frame = self.ghost_frames[self.current_ghost]
        else:
            frame = self.dead_img
        self.screen.blit(frame, (self.x, self.y))
        for i in range(self.lives):
            self.screen.blit(self.heart_frames[self.current_heart], (15 + i * (50 + 5), 20))

    def minus_life(self, laser: Laser):
        laser_rect = pygame.transform.rotate(laser.frames[laser.current_frame], laser.angle).get_rect(center=(laser.x, laser.y))
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if player_rect.colliderect(laser_rect):
            return True
        return False

    def die(self):
        if not self.dead or self.death_time is None:
            return False
        now = pygame.time.get_ticks()
        if now - self.death_time >= 2000:
            return True
        return False
    def death_sound(self):
        self.death_s.play()

class Squares:
    def __init__(self, sq_list : list, screen : pygame.Surface):
        self.square_list = sq_list
        self.check_btn = pygame.image.load('imgs/check.png')
        self.check_btn = pygame.transform.smoothscale_by(self.check_btn, 0.18)
        self.sc = screen
        self.btn_fl = False
        self.work_fl = True
        self.square_for_check = None
        self.y = self.sc.get_height() - self.check_btn.get_height() - 18
        self.last_time = None
        self.bad_st = None
        font_bad = pygame.font.Font('fonts/Handjet.ttf', 28)
        self.bad_text = font_bad.render('Упс! Ты попал на плохой квадрат))', True, (0, 0, 0), (202, 179, 208))
        self.bad_fl_text = False
        self.cats = []
        self.cats_frames = [pygame.transform.scale_by(pygame.image.load(f'cat/maxwell-cat-{i}.png'), 1.2) for i in range(187)]
        self.cat_fl = False
        self.cat_frame = 0
        self.anim_st_cat = None
        self.bg_cat = pygame.image.load('imgs/bg_cat.png')
        self.bg_cat = pygame.transform.scale(self.bg_cat, (900, 600))
        self.pop_fl = False
        self.cat_st = None
        self.visited_pas = []
        self.level_complete = False
        self.pas = []
        self.found_text = None
        c_cats = 0
        c_not = 0
        self.found_cats = [] 
        exp = []
        while c_cats != 5:
            r = randint(0, 14)
            if r not in exp:
                self.cats.append(r)
                exp.append(r)
                c_cats += 1
        while c_not != 10:
            r = randint(0, 14)
            if r not in exp:
                self.pas.append(r)
                exp.append(r)
                c_not += 1
        self.cats.sort()
        self.pas.sort()
    def check_player(self, player : Player):
        i = 0
        for sq in self.square_list:
            if (player.x >= sq[0] and player.x <= sq[0] + 100) and (player.y >= sq[1] and player.y <= sq[1] + 100):
                if sq not in self.visited_pas and sq not in self.found_cats:
                    self.btn_fl = True
                    self.square_for_check = i
                    break
            i += 1
    def blit_btn(self):
        if self.btn_fl and self.work_fl:
            self.sc.blit(self.check_btn, (70, self.y))  
            self.btn_fl = False
            
    def check_square(self, time, player : Player):
        if self.square_for_check is None:
            return

        if self.last_time is None or time - self.last_time >= 400:
            self.last_time = time
            if self.square_for_check in self.cats:
                self.cat_fl = True
                self.found_cats.append(self.square_for_check) 
                self.cats.remove(self.square_for_check)  
                print(f'cat with index {self.square_for_check} and coords {self.square_list[self.square_for_check]}')
                if not self.cats: 
                    self.level_complete = True
            elif self.square_for_check in self.pas:
                self.bad_fl_text = True
                player.lives -= 1
                player.death_sound()
                self.visited_pas.append(self.square_for_check)
                self.pas.remove(self.square_for_check)
                print(f'bad with index {self.square_for_check} and coords {self.square_list[self.square_for_check]}')
            else:
                print(f'already checked with index{self.square_for_check} and coords {self.square_list[self.square_for_check]}' )


    def draw_cat(self, player : Player, time, font : pygame.font.Font):
        if self.cat_fl:

            if self.cat_st is None:
                self.cat_st = time
                self.anim_st_cat = time
                self.found_text = font.render(f'Найдено котов: {len(self.found_cats)} / 5', True, (244, 30, 23))
            self.sc.blit(self.bg_cat, (0, 0))
            self.sc.blit(self.cats_frames[self.cat_frame], (320, 230))
            self.sc.blit(self.found_text, (900 / 2 - self.found_text.get_width() / 2, 500))
            if time - self.anim_st_cat >= 90:
                self.cat_frame = (self.cat_frame + 1) % 187
                self.anim_st_cat = time

            if time - self.cat_st >= 3100:
                self.cat_fl = False
                self.square_for_check = None
                self.cat_st = None
                self.cat_frame = 0
                self.anim_st_cat = None

    def draw(self, time):
        for i, sq in enumerate(self.square_list):
            if i in self.found_cats:
                pygame.draw.rect(self.sc, (0, 255, 0), (sq[0], sq[1], 100, 100)) 
            elif i in self.visited_pas:
                pygame.draw.rect(self.sc, (0, 0, 0), (sq[0], sq[1], 100, 100))  

    def draw_bad_text(self, time):
        if self.bad_fl_text:
            if self.bad_st is None:
                self.bad_st = time
            self.sc.blit(self.bad_text, (900 - self.bad_text.get_width() - 40, 20))  
            if time - self.bad_st >= 1700:
                self.bad_fl_text = False
                self.bad_st = None
        
        
        
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
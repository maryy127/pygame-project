import pygame
from time import sleep
from functions import *
name = 'Маша'
#name = input('Введите свое имя:  ')
name = name.capitalize()
pygame.init()

# Код, описывающий окно программы
w= 900  
h = 600  
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption('my game')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
# Создаём контроль FPS
clock = pygame.time.Clock()
FPS = 30  # Устанавливаем нужное значение FPS

#loading state variables 
state = 'instruction'
font1 = pygame.font.Font('fonts/Handjet.ttf', 60)
font2 = pygame.font.Font('fonts/Handjet.ttf', 34)
wellcome = font1.render(f'WELLCOME {name.upper()}', True, (14, 88, 52))
visible_w = True
last_blink_time = pygame.time.get_ticks()
BLINK_INTERVAL = 400
bar_speed = 3
bar_x = 0
text_display = 'LOADING.......'
current_index = 0
last_update_time = pygame.time.get_ticks()
complete_fl = False

#rules
rules_font1 = pygame.font.Font('fonts/Comfortaa.ttf', 24)
header_r = font1.render('правила игры'.upper(), True, (220, 72, 161))
text_rules_list = render_wrapped_text(w, header_r.get_height() + 70, f'Привет, {name}! Сегодня тебе предстоит сыграть в увлекательную игру. Тут тебе предстоит пройти три уровня, на каждом из которых ты должен будешь найти трофей, используя магическую силу рандома. Трофей располагается только в двух квадратах из 15! У тебя есть всего три жизни для каждого из уровней. Также иногда могут появлятся пасхалки, берегись их, они опасны. Ну что же, начинаем!', rules_font1, (230, 168, 199), 880, 19, (191, 0, 255), 1)
press_to_c = font2.render('press any key to start the game'.upper(), True, (255, 255, 255))
press_y = text_rules_list[-1][1][1] + text_rules_list[-1][0].get_height() + 47
#game imgs
bg_rules = pygame.image.load('rules_bg.jpg')
bg_game = pygame.image.load('bg_game.jpg')
squares_game = pygame.image.load('squares_game.svg')
#spider animation
num_i = 0
slow = 3
spider_list = [pygame.image.load(f'spider/frame-{i}.gif') for i in range(1, 9)]
#ghost animation
ghost_list = [pygame.image.load(f'ghost/frame-{i}.gif') for i in range(1, 13)]
gh_x = 150 
gh_y = 115
gh_speed = 9
move_up_flag = False #vychitaniye
move_down_fl = False
move_left_fl = False
move_right_fl = False
#heart anim
heart_list = [pygame.image.load(f'pixel_heart/frame-{i}.gif') for i in range(1, 10)]
lives_c = 3
he_x = 20
# laser pashalko))))))))))))))))
laser_list = [f'laser/frame-{i}.gif' for i in range(1, 5)]
laser = Laser(0, 0, 900, 600, 150, laser_list, 130)
colider_fl = False
new_laser = 0
# Игровой цикл и флаг выполнения программы
laser_fl = False
game_run = True
while game_run:
    dt = clock.tick(FPS)
    # БЛОК ОБРАБОТКИ СОБЫТИЙ ИГРЫ
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move_up_flag = True
            if event.key == pygame.K_DOWN:
                move_down_fl = True
            if event.key == pygame.K_RIGHT:
                move_right_fl = True
            if event.key == pygame.K_LEFT:
                move_left_fl = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                move_up_flag = False
            if event.key == pygame.K_DOWN:
                move_down_fl = False
            if event.key == pygame.K_RIGHT:
                move_right_fl = False
            if event.key == pygame.K_LEFT:
                move_left_fl = False
    keys = pygame.key.get_pressed()

    if state == 'loading':
        if bar_x < (480):
            bar_x += bar_speed
        else:
            complete_fl = True
        screen.fill((73, 42, 72))
        # wellcome
        if current_time - last_blink_time >= BLINK_INTERVAL:
            visible_w = not visible_w
            last_blink_time = current_time
        
        # loading bar
        if current_time - last_update_time >= BLINK_INTERVAL and current_index < len(text_display):
            current_index += 1
            last_update_time = current_time

        if visible_w:
            screen.blit(wellcome, ((w/2 - wellcome.get_width() / 2), 100))
        pygame.draw.rect(screen, (39,72,0), (w / 2 - 250, 250, 500, 100), 7)
        pygame.draw.rect(screen, (46,105,32), (w/2 - 250 + 10, 260, bar_x, 80))
        text_load = font2.render(text_display[:current_index], True, (255, 255, 255))
        if complete_fl:
            text_load = font2.render('LOADING COMPLETE!', True, (255, 100, 55))
        screen.blit(text_load, ((w / 2 - text_load.get_width() / 2), 250 + text_load.get_height() + 100))
        if complete_fl:
            screen.blit(wellcome, ((w/2 - wellcome.get_width() / 2), 100))
            pygame.display.flip()
            sleep(1.2)
            state = 'instruction'



    elif state == 'instruction':
        # blinking press
        if current_time - last_blink_time >= BLINK_INTERVAL:
            visible_w = not visible_w
            last_blink_time = current_time

        screen.blit(bg_rules, (0, 0))
        screen.blit(header_r, (w / 2 - header_r.get_width() / 2, 25))
        for t in text_rules_list:
            screen.blit(t[0], t[1])
        if visible_w:
            screen.blit(press_to_c, (w / 2 - press_to_c.get_width() / 2, press_y))
        if any(keys):
            state='game'
            game_start_time = pygame.time.get_ticks()

    elif state == 'game':
        # animation
        num_i += 1
        num_frame_spider = num_i // slow % 8
        num_frame_gh = num_i // slow % 12
        num_frame_heart = num_i // slow % 9
        num_frame_laser = num_i // slow % 4
        laser_rect = pygame.transform.rotate(laser.frames[laser.current_frame], laser.angle).get_rect(center=(laser.x, laser.y))
        player_rect = pygame.Rect(gh_x, gh_y, ghost_list[0].get_width(), ghost_list[0].get_height())

        # move pers
        if move_up_flag:
            gh_y = max(100, gh_y - gh_speed)
        if move_down_fl:
            gh_y = min(480 - 80, gh_y + gh_speed)      # 480 – высота границы, 80 – высота спрайта
        if move_left_fl:
            gh_x = max(140, gh_x - gh_speed)            # минимальная x = 140
        if move_right_fl:
            gh_x = min(800 - 80, gh_x + gh_speed)
        # laser
        if current_time >= 3500 and not colider_fl:
            laser.update(dt)
            laser_fl=True
        if player_rect.colliderect(laser_rect) and not colider_fl:
            lives_c -= 1
            laser_fl = False
            colider_fl = True
            new_laser = current_time

        if current_time - new_laser >= 3700:
            colider_fl = False
        screen.blit(bg_game, (0, 0))
        screen.blit(squares_game, (0, 0))
        screen.blit(spider_list[num_frame_spider], (800, 0))
        screen.blit(ghost_list[num_frame_gh], (gh_x, gh_y))
        if laser_fl and not colider_fl:
            laser.draw(screen)
        for i in range(lives_c):
            screen.blit(heart_list[num_frame_heart], (he_x + i * (60 + 5), 20))
    pygame.display.flip() 

pygame.quit()
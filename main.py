# -*- coding: utf-8 -*-
import pygame
from functions import *

name = input('Введите свое имя:  ')
name = name.capitalize()

pygame.init()
pygame.mixer.init()
game_start_sound = pygame.mixer.Sound('sfx/game_start.wav')
laser_shift_sound = pygame.mixer.Sound("sfx/laser_shift.wav")
death_sound = pygame.mixer.Sound("sfx/player_die.wav")

# Код, описывающий окно программы
w= 900  
h = 600  
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption('ghost game')
icon = pygame.image.load('imgs/icon.png')
pygame.display.set_icon(icon)
# Создаём контроль FPS
clock = pygame.time.Clock()
FPS = 30  # Устанавливаем нужное значение FPS

#loading state variables 
font1 = pygame.font.Font('fonts/Handjet.ttf', 60)
font2 = pygame.font.Font('fonts/Handjet.ttf', 34)
wellcome = font1.render(f'WELLCOME TO GHOST GAME', True, (14, 88, 52))
logo = pygame.transform.scale(icon, (200, 200))
visible_w = True
last_blink_time = pygame.time.get_ticks()
BLINK_INTERVAL = 400
bar_speed = 3
bar_x = 0
text_display = 'LOADING.......'
current_index = 0
last_update_time = pygame.time.get_ticks()
complete_fl = False
time_loaded_added = False

#rules
rules_font1 = pygame.font.Font('fonts/Comfortaa.ttf', 24)
header_r = font1.render('правила игры'.upper(), True, (220, 72, 161))
text_rules_list = render_wrapped_text(w, header_r.get_height() + 100, f'Привет, {name}! Сегодня тебе предстоит сыграть в увлекательную игру. Тут тебе предстоит найти трофей, используя магическую силу рандома. Трофей располагается только в пяти квадратах из 15! У тебя есть всего пять жизней. Также тут есть злой лазер из королевства Zлой Кола, берегись eгo, он опасен. Hy что же, начинаем!', rules_font1, (230, 168, 199), 880, 19, (191, 0, 255), 1)
press_to_c = font2.render('press any key to start the game'.upper(), True, (255, 255, 255))
press_y = text_rules_list[-1][1][1] + text_rules_list[-1][0].get_height() + 47

#game imgs
bg_rules = pygame.image.load('imgs/rules_bg.jpg')
bg_game = pygame.image.load('imgs/bg_game.jpg')
squares_game = pygame.image.load('imgs/squares_game.svg')

game_over = pygame.image.load('imgs/game_over.png')
restart_btn = pygame.image.load('imgs/restart.png')
restart_btn.set_colorkey((255, 255, 255))
restart_btn = pygame.transform.scale(restart_btn, (100, 100))

#spider animation
num_i = 0
slow = 3
spider_list = [pygame.image.load(f'spider/frame-{i}.gif') for i in range(1, 9)]

#player
ghost_list = [f'ghost/frame-{i}.gif' for i in range(1, 13)]
heart_list = [f'pixel_heart/frame-{i}.gif' for i in range(1, 10)]

player = Player(ghost_list, heart_list, 150, 115, 9, 5, screen, [140, 100, 800, 480], 'imgs/dead_player.png')

# laser)
laser_list = [f'laser/frame-{i}.gif' for i in range(1, 5)]
laser = Laser(0, 0, 900, 600, 150, laser_list, laser_shift_sound, 130)
colider_fl = False
new_laser = 0
laser_fl = False
laser_start_time = 0
game_start_time = 0
wait_laser = randint(1600, 3000)

#squares
sq_list = []
x_sq, y_sq = 140, 100
for lines in range(3):
    for sq in range(5):
        sq_list.append([x_sq, y_sq])
        x_sq += 140
    x_sq = 140
    y_sq += 140
    
squares = Squares(sq_list, screen)
check_btn_fl = False

# win
win_text = font1.render('УРА ПОБЕДА!', True, (255, 42, 42), (255, 255, 0))
win_img = pygame.image.load('imgs/win.png')
kubok = pygame.image.load('imgs/kubok.png')
win_img.set_colorkey((255, 255, 255))
win_img = pygame.transform.scale_by(win_img, 0.39)
# Игровой цикл и флаг выполнения программы
state = 'loading'
game_run = True

while game_run:
    dt = clock.tick(FPS)
    current_time = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if state == 'game':
                if (pos[0] >= 70 and pos[0] <= 70 + squares.check_btn.get_width()) and (pos[1] >= squares.y and pos[1] <= squares.y + squares.check_btn.get_height()):
                    check_btn_fl = True
            if state == 'game_over':
                if (pos[0] >= w / 2 - 50 and pos[0] <= w / 2 - 50 + 100) and (pos[1] >= 400 and pos[1] <= 500):
                    player = Player(ghost_list, heart_list, 150, 115, 9, 5, screen, [140, 100, 800, 480], 'imgs/dead_player.png')
                    laser = Laser(0, 0, 900, 600, 150, laser_list, laser_shift_sound, 130)
                    squares = Squares(sq_list, screen)
                    colider_fl = False
                    new_laser = 0
                    laser_fl = False
                    game_start_time = current_time
                    wait_laser = randint(1600, 3000)
                    print('-' * len('bad with index 11 and coords [280, 380]'))
                    print('game restarted')
                    state = 'game'
            if state == 'level_complete':
                 if (pos[0] >= w / 2 - 50 and pos[0] <= w / 2 - 50 + 100) and (pos[1] >= 350 and pos[1] <= 350 + 100):
                    player = Player(ghost_list, heart_list, 150, 115, 9, 5, screen, [140, 100, 800, 480], 'imgs/dead_player.png')
                    laser = Laser(0, 0, 900, 600, 150, laser_list, laser_shift_sound, 130)
                    squares = Squares(sq_list, screen)
                    colider_fl = False
                    new_laser = 0
                    laser_fl = False
                    game_start_time = current_time
                    wait_laser = randint(1600, 3000)
                    print('-' * len('bad with index 11 and coords [280, 380]'))
                    print('game restarted')
                    state = 'game'


    if state == 'loading':
        if bar_x < (480):
            bar_x += bar_speed
        else:
            complete_fl = True

        screen.fill((73, 42, 72))
        screen.blit(logo, (w / 2 - logo.get_width() / 2, 20))
        # wellcome
        if current_time - last_blink_time >= BLINK_INTERVAL:
            visible_w = not visible_w
            last_blink_time = current_time
        
        # loading bar
        if current_time - last_update_time >= BLINK_INTERVAL and current_index < len(text_display):
            current_index += 1
            last_update_time = current_time

        if visible_w:
            screen.blit(wellcome, ((w/2 - wellcome.get_width() / 2), logo.get_height() + 20 + 20))
        pygame.draw.rect(screen, (39,72,0), (w / 2 - 250, logo.get_height() + wellcome.get_height() + 20 + 20 + 30, 500, 100), 7)
        pygame.draw.rect(screen, (46,105,32), (w/2 - 250 + 10, logo.get_height() + 20 + 20 + 30 + 10 + wellcome.get_height(), bar_x, 80))
        text_load = font2.render(text_display[:current_index], True, (255, 255, 255))
        if complete_fl:
            text_load = font2.render('LOADING COMPLETE!', True, (255, 100, 55))

        screen.blit(text_load, ((w / 2 - text_load.get_width() / 2), logo.get_height() + 20 + 20 + 30 + 10 + 30 + wellcome.get_height() * 2 + 30))
        if complete_fl:
            screen.blit(wellcome, ((w/2 - wellcome.get_width() / 2), logo.get_height() + 20 + 20))
            if not time_loaded_added:
                game_start_sound.play()
                time_loaded = current_time
                time_loaded_added = True
            if current_time - time_loaded >= 1400:
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
            game_start_time = current_time

    elif state == 'game':
        # animation
        num_i += 1
        num_frame_spider = num_i // slow % 8
        player.current_heart = num_i // slow % 9
        num_frame_laser = num_i // slow % 4

        # move pers
        player.update(keys)

        #squares
        if not squares.cat_fl:
            squares.check_player(player)
        if check_btn_fl and not squares.cat_fl:
            squares.check_square(current_time, player)
            check_btn_fl = False

        # laser
        if (current_time - game_start_time >= wait_laser) and (not colider_fl) and (not squares.cat_fl) and (not player.dead):
            laser.update(dt)
            laser_fl=True

        if player.minus_life(laser) and (not colider_fl) and (not player.dead) and (not squares.cat_fl):
            player.lives -= 1
            death_sound.play()
            laser_fl = False
            colider_fl = True
            new_laser = current_time

        if player.lives < 1:
                if player.dead:
                    if player.die():
                        state = 'game_over'
                else:
                    player.dead = True
                    squares.work_fl = False
                    player.death_time = pygame.time.get_ticks()
                    death_sound.play()


        if current_time - new_laser >= 2300 and not player.dead:
            colider_fl = False

        screen.blit(bg_game, (0, 0))
        screen.blit(squares_game, (0, 0))
        squares.draw(current_time)
        screen.blit(spider_list[num_frame_spider], (800, 0))
        player.draw()

        if laser_fl and not colider_fl and (not squares.cat_fl) and (not player.dead):
            laser.draw(screen)
        squares.blit_btn()
        squares.draw_bad_text(current_time)
        if squares.cat_fl:
            squares.draw_cat(player, current_time, font1)
        if squares.level_complete and not squares.cat_fl:
            state = 'level_complete'

    elif state == 'game_over':
        screen.fill((213, 52, 100))
        screen.blit(game_over, (0, 0))
        screen.blit(restart_btn, (w / 2 - 50, 400))

    elif state == 'level_complete':
        screen.fill((50, 168, 82))  
        screen.blit(win_img, (w/2 - win_img.get_width() / 2, h/2 - win_img.get_height() / 2))
        screen.blit(kubok, (w/2 - kubok.get_width() / 2, h/2 - kubok.get_height() / 2))
        screen.blit(win_text, (w / 2 - win_text.get_width() / 2, 190))
        pygame.draw.rect(screen, (204, 20, 32), (w /2 - 50, 350, restart_btn.get_width(), restart_btn.get_height()), width=0, border_radius=70)
        screen.blit(restart_btn, (w / 2 - 50, 350))
        


    pygame.display.flip() 

pygame.quit()

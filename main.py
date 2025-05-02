import pygame
from time import sleep
from functions import *
name = 'Маша'
#name = input('Введите свое имя:  ')
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
pygame.display.set_caption('my game')
icon = pygame.image.load('imgs/icon.png')
pygame.display.set_icon(icon)
# Создаём контроль FPS
clock = pygame.time.Clock()
FPS = 30  # Устанавливаем нужное значение FPS

#loading state variables 
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
time_loaded_added = False

#rules
rules_font1 = pygame.font.Font('fonts/Comfortaa.ttf', 24)
header_r = font1.render('правила игры'.upper(), True, (220, 72, 161))
text_rules_list = render_wrapped_text(w, header_r.get_height() + 70, f'Привет, {name}! Сегодня тебе предстоит сыграть в увлекательную игру. Тут тебе предстоит пройти три уровня, на каждом из которых ты должен будешь найти трофей, используя магическую силу рандома. Трофей располагается только в двух квадратах из 15! У тебя есть всего три жизни для каждого из уровней. Также иногда могут появлятся пасхалки, берегись их, они опасны. Ну что же, начинаем!', rules_font1, (230, 168, 199), 880, 19, (191, 0, 255), 1)
press_to_c = font2.render('press any key to start the game'.upper(), True, (255, 255, 255))
press_y = text_rules_list[-1][1][1] + text_rules_list[-1][0].get_height() + 47
print(text_rules_list)

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

player = Player(ghost_list, heart_list, 150, 115, 9, 3, screen, [140, 100, 800, 480], 'imgs/dead_player.png')

# laser)
laser_list = [f'laser/frame-{i}.gif' for i in range(1, 5)]
laser = Laser(0, 0, 900, 600, 150, laser_list, laser_shift_sound, 130)
colider_fl = False
new_laser = 0
laser_fl = False
laser_start_time = 0
game_start_time = 0

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
            if state == 'game_over':
                pos = pygame.mouse.get_pos()
                if (pos[0] >= w / 2 - 50 and pos[0] <= w / 2 - 50 + 100) and (pos[1] >= 400 and pos[1] <= 500):
                    player = Player(ghost_list, heart_list, 150, 115, 9, 3, screen, [140, 100, 800, 480], 'imgs/dead_player.png')
                    laser = Laser(0, 0, 900, 600, 150, laser_list, laser_shift_sound, 130)
                    colider_fl = False
                    new_laser = 0
                    laser_fl = False
                    game_start_time = current_time
                    state = 'game'

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
        # laser
        if current_time - game_start_time >= 3000 and not colider_fl:
            laser.update(dt)
            laser_fl=True

        if player.minus_life(laser) and not colider_fl and not player.dead:
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
                    player.death_time = pygame.time.get_ticks()
                    death_sound.play()


        if current_time - new_laser >= 2300 and not player.dead:
            colider_fl = False

        screen.blit(bg_game, (0, 0))
        screen.blit(squares_game, (0, 0))
        screen.blit(spider_list[num_frame_spider], (800, 0))
        player.draw()
        if laser_fl and not colider_fl:
            laser.draw(screen)
    
    elif state == 'game_over':
        screen.fill((213, 52, 100))
        screen.blit(game_over, (0, 0))
        screen.blit(restart_btn, (w / 2 - 50, 400))

    pygame.display.flip() 

pygame.quit()
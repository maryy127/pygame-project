import pygame
from time import sleep

name = '0'
#name = input('Введите свое имя:  ')
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
state = 'game'
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
# Игровой цикл и флаг выполнения программы
game_run = True
while game_run:

    # БЛОК ОБРАБОТКИ СОБЫТИЙ ИГРЫ
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if gh_y > 200 + ghost_list[0].get_height() + 50:
                    move_up_flag = True
            if event.key == pygame.K_DOWN:
                if gh_y < 480 - ghost_list[0].get_height():
                    move_down_fl = True
            if event.key == pygame.K_RIGHT:
                if gh_x < 790 + 80:
                    move_right_fl = True
            if event.key == pygame.K_LEFT:
                if gh_x > 150:
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
            state = 'instuction'


    elif state == 'instuction':
        screen.blit(bg_rules, (0, 0))
        if any(keys):
            state='game'

    elif state == 'game':

        num_i += 1
        num_frame_spider = num_i // slow % 8
        num_frame_gh = num_i // slow % 12
        if move_up_flag:
            gh_y -= gh_speed
        if move_down_fl:
            gh_y += gh_speed
        if move_left_fl:
            gh_x -= gh_speed
        if move_right_fl:
            gh_x += gh_speed

        screen.blit(bg_game, (0, 0))
        screen.blit(squares_game, (0, 0))
        screen.blit(spider_list[num_frame_spider], (800, 0))
        screen.blit(ghost_list[num_frame_gh], (gh_x, gh_y))
    pygame.display.flip() 
    clock.tick(FPS)  # Контроль FPS

pygame.quit()
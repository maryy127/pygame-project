from functions import *
import pygame
from time import sleep

pygame.init()

# Код, описывающий окно программы
w= 900  
h = 700  
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption('my game')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
# Создаём контроль FPS
clock = pygame.time.Clock()
FPS = 30  # Устанавливаем нужное значение FPS

#loading state variables 
state = 'loading'
font1 = font.Font('fonts/Handjet.ttf', 60)
font2 = font.Font('fonts/Handjet.ttf', 34)
wellcome = font1.render('WELLCOME USER', True, (14, 88, 52))
visible_w = True
last_blink_time = pygame.time.get_ticks()
BLINK_INTERVAL = 400
bar_speed = 3
bar_x = 0
text_display = 'LOADING.......'
current_index = 0
last_update_time = pygame.time.get_ticks()
complete_fl = False
# Игровой цикл и флаг выполнения программы
game_run = True
while game_run:

    # БЛОК ОБРАБОТКИ СОБЫТИЙ ИГРЫ
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_run = False


    # changing variables
    if bar_x < (480):
        bar_x += bar_speed
    else:
        complete_fl = True


    if state == 'loading':
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
        pygame.draw.rect(screen, (39,72,0), (w / 2 - 250, 300, 500, 100), 7)
        pygame.draw.rect(screen, (46,105,32), (w/2 - 250 + 10, 310, bar_x, 80))
        text_load = font2.render(text_display[:current_index], True, (255, 255, 255))
        if complete_fl:
            text_load = font2.render('LOADING COMPLETE!', True, (255, 100, 55))
        screen.blit(text_load, ((w / 2 - text_load.get_width() / 2), 300 + text_load.get_height() + 100))
        if complete_fl:
            screen.blit(wellcome, ((w/2 - wellcome.get_width() / 2), 100))
            pygame.display.flip()
            sleep(1.2)
            state = 'instuction'


    if state == 'instuction':
        screen.fill((96, 17, 94))


    pygame.display.flip() 
    clock.tick(FPS)  # Контроль FPS

pygame.quit()
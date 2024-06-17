import pygame
import os 
import random
import sys
import pygame.mixer
from modules.classes import *
from modules.mapsetting import map

pygame.init() #дозволяє використовувати внутрішні модулі pygame

background = pygame.image.load(os.path.join(PATH, 'images/background.png'))
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)) #буде підлаштовувати картинку під потрібні розміри


# Ініціалізація звуку
pygame.mixer.init()

# Завантаження звуків
shoot_sound = pygame.mixer.Sound(os.path.join(PATH, 'sounds', 'strike.wav')) #постріл
win_sound = pygame.mixer.Sound(os.path.join(PATH, 'sounds', 'back_music.wav')) #перемога
tank_sound = pygame.mixer.Sound(os.path.join(PATH, 'sounds', 'tank_sound.wav')) #звук їзди танка
wall_break_sound = pygame.mixer.Sound(os.path.join(PATH, 'sounds', 'wall_break.wav')) #руйнування стінки
tank_break_sound = pygame.mixer.Sound(os.path.join(PATH, 'sounds', 'tank_break.wav')) #попадання в танк

#задаєм шрифт за класом Font(назва і розмір)
font = pygame.font.Font(None, 120)
winner1_text = font.render('BlUE WIN', True, (0, 0, 255)) #перетворюєм текст в картинку
winner2_text = font.render('RED WIN', True, (255, 0, 0))
close = font.render("exit", True, (255, 255, 255))
close_rect = close.get_rect(topleft=(32, (background.get_height()-32)-64))



x = 0 #це початок координат (0,0)
y = 0
blocks_list = [] #список який буде в собі зберігати об'єкти блоків

wall_image1 = os.path.join(PATH, 'images/wall.png')
wall_image2 = os.path.join(PATH, 'images/wall1.png')



#Цей цикл генерує карту
for row in map: #кожен рядок в матриці перебираєм
    for i in row: #перебираєм кожен елемент з рядка
        if i == 1: # Якщо елемент матриці дорівнює 1, то додаємо блок з координатами x, y і типом 1
            blocks_list.append(Block(x, y, 1, wall_image1)) #додаєм блок з координатами x,y
        elif i == 2:  # Якщо елемент матриці дорівнює 2, то додаємо блок з координатами x, y і типом 2
            blocks_list.append(Block(x, y, 2, wall_image2)) #змінили тип і картинку   
        x += STEP   # Збільшуємо x, рухаємося по рядку вправо
    y += STEP   #збільшуєм y, йдемо вниз
    x = 0 # Скидаємо x до початкового значення для початку нового рядка


player1 = Player(1,1) #від класу Player (в лівому верхньому куту)
player2 = Player2(26, 14) 

clock = pygame.time.Clock() #створює об'єкт годинника, який дозволить контролювати швидкість оновлення гри.

winner = 0
is_winner = True  # Визначення змінної для перевірки переможця
menu = True # Змінна, що вказує на те, чи відображається меню




is_game_running = True  # вказує на те, що гра триває 

while is_game_running:  # циикл, який виконується, доки гра триває
        
    window.blit(background, (0,0)) # координати для картинки 
    # Перевірка зіткнення кулі гравця 1 та 2 з блоком
    for block in blocks_list: #проходить через кожен елемент у списку 
        block.blit() # відображення блоку на вікні
        if block.colliderect(player1.bullet): # перевірка зіткнення блоку з кулею гравця 1
            player1.bullet.stop() # зупинка кулі
            if block.type_block == 1: # перевірка, чи зруйнований блок(1-можна зруйнувати)
                map[block.y // STEP][block.x // STEP] = 0  # оновлення карти
                block.x = 1000000 # позиція блоку встановлюється на велике значення, щоб блок зник з екрану після руйнування
                wall_break_sound.play() # відтворення звуку руйнування стіни


        if block.colliderect(player2.bullet): # перевірка зіткнення блоку з кулею гравця 2
            player2.bullet.stop()  # зупинка кулі
            if block.type_block == 1: #1-це блоки який можна зруйнувати
                map[block.y // STEP][block.x // STEP] = 0
                block.x = 1000000
                wall_break_sound.play()

    player1.bullet.move() # переміщення кулі гравця 1
    player2.bullet.move() 

        
    player1.blit()  # відображення гравця 1 
    player2.blit()  

    # Відтворення звуку при вистрілі
    keys = pygame.key.get_pressed()
    if keys[pygame.K_c]:
        shoot_sound.play()
    elif keys[pygame.K_SPACE]:
        shoot_sound.play()

    # Відтворення звуку під час руху танків
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]:
        tank_sound.play() 
    if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
        tank_sound.play()  


    #взаємодія між кулею і гравцем
    if player1.colliderect(player2.bullet): #якщо player1 торкнувся player2.bullet
        tank_break_sound.play() # Відтворення звуку руйнування танка
        win_sound.play()
        winner = 1  # Якщо переміг player1
        is_game_running = False # Зупинка гри
        is_winner = True # Оголошення переможця
    elif player2.colliderect(player1.bullet): # Якщо player2 торкнувся player1.bullet
        tank_break_sound.play()
        win_sound.play()  
        winner = 2 # Якщо переміг player2
        is_game_running = False #коли один попадає в іншого танка, то х гри відбувається вихід
        is_winner = True # Оголошення переможця

    # Обробка подій від pygame    
    for event in pygame.event.get(): # Отримує всі події, що сталися в грі
        if event.type == pygame.QUIT:  # Якщо користувач натиснув на кнопку закриття вікна
            is_game_running = False  # Зупинка гри
        
    pygame.display.flip() # Оновлення відображення екрану
    clock.tick(10) # Обмеження частоти кадрів до 10 кадрів за секунду


# Визначення початкової позиції тексту переможця на екрані
cors = (SCREEN_WIDTH // 2 - winner1_text.get_width() // 2,     # Горизонтальне центрування тексту переможця
        SCREEN_HEIGHT // 2 - winner1_text.get_height() // 2)   # Вертикальне центрування тексту переможця

while is_winner: # Поки є переможець
    window.blit(background, (0, 0)) # Відображення фону
    if winner == 2: 
        window.blit(winner1_text, cors) # Відображення тексту переможця
        
    elif winner == 1:
        window.blit(winner2_text, cors)

    # Обробка подій
    for event in pygame.event.get():
        # Якщо користувач натиснув кнопку закриття вікна
        if event.type == pygame.QUIT:
            is_winner = False # Зупинка гри
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and menu:  # Перевірка чи натиснута ліва кнопка миші і чи відображається меню

                # Перевірка, чи користувач клікнув на кнопку закриття
                if close_rect.collidepoint(event.pos):
                    is_winner = False # Закриття вікна
            
     # Якщо є відображене меню, то відображаємо кнопку закриття
    if menu:
        background.blit(close, (32, (background.get_height()-32)-64))
        
    
    pygame.display.flip() # Оновлення відображення екрану
    clock.tick(60) # Обмеження частоти кадрів на секунду


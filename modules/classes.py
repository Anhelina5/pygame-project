import pygame  # Імпортуємо бібліотеку pygame для роботи з графікою
import os  # Імпортуємо модуль os для роботи з операційною системою
from modules.mapsetting import map  # Імпортуємо map з іншого модуля

PATH = os.path.abspath(__file__ + '/../..')  # Визначаємо шлях до кореневої директорії гри



SCREEN_WIDTH = 1400  # Ширина вікна гри
SCREEN_HEIGHT = 800  # Висота вікна гри
STEP = 50  # Розмір кроку для карти

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Ініціалізуємо вікно гри 
pygame.display.set_caption('Tanks 2D') # Встановлюємо заголовок вікна гри

# Клас Block, який є підкласом pygame.Rect
class Block(pygame.Rect):
    def __init__(self, x, y, type_block, image): 
        # Ініціалізуємо клас Block як підклас pygame.Rect
        super().__init__(x, y, STEP, STEP) # Ініціалізуємо батьківський клас pygame.Rect з вказаними координатами і розміром
        self.image = pygame.image.load(image)  
        self.image = pygame.transform.scale(self.image, (STEP, STEP))  # Змінюємо розмір зображення
        self.type_block = type_block  # Встановлюємо тип блоку

    def blit(self):
        window.blit(self.image, (self.x, self.y))  # Рисуємо блок на екрані гри в позиції (self.x, self.y)


class Bullet(pygame.Rect):
    def __init__(self, x, y):
        # Ініціалізуємо клас Bullet як підклас pygame.Rect
        super().__init__(x, y, 20, 20)
        self.image = pygame.image.load(os.path.join(PATH, 'images/bullet.png')) 
        self.image = pygame.transform.scale(self.image, (20, 20))  # Змінюємо розмір зображення кулі
        self.direction = None  # Напрямок руху кулі
        self.speed = 60  # Швидкість руху кулі
        self.count = 0  # Лічильник для керування рухом кулі

    def move(self):
        # Рухаємо кулю в заданому напрямку
        if self.count != 0:  # Перевіряємо, чи куля ще має рухатися
            window.blit(self.image, (self.x, self.y))  # Відображаємо зображення кулі на позиції (x, y)
            if self.direction == 0:  # Якщо напрямок руху вгору
                self.y -= self.speed  # Зміщуємо кулю вгору на відстань, визначену швидкістю
            elif self.direction == 180:  # Якщо напрямок руху вниз
                self.y += self.speed  # Зміщуємо кулю вниз на відстань, визначену швидкістю
            elif self.direction == 90:  # Якщо напрямок руху вліво
                self.x -= self.speed  # Зміщуємо кулю вліво на відстань, визначену швидкістю
            elif self.direction == 270:  # Якщо напрямок руху вправо
                self.x += self.speed  # Зміщуємо кулю вправо на відстань, визначену швидкістю
            self.count -= 1  # Зменшуємо лічильник руху кулі
            if self.count == 0:  # Якщо лічильник досягнув нуля
                self.stop()  # Зупиняємо рух кулі

            
    def stop(self): # Функція для зупинки руху кулі
        self.count = 0  # Скидаємо лічильник кулі
        self.x = 100000  # Поміщаємо кулю за межами екрану, щоб вона більше не була видимою


class Panzar(pygame.Rect):
    def __init__(self, x, y):
        # Ініціалізуємо клас Panzar як підклас pygame.Rect
        super().__init__(x * STEP, y * STEP, STEP, STEP)  # Викликаємо конструктор батьківського класу pygame.Rect з позиціями і розмірами блоку
        self.image = None  # Зображення танка
        self.pos = [x, y]  # Позиція панцера на карті
        self.bullet = Bullet(x, y)  # Об'єкт кулі
        self.angle = 0  # Кут повороту панцера
        self.speed = 5  # Швидкість руху панцера

    def move(self):
        pass  

    def blit(self):
        self.move()  # Викликаємо метод для руху панцера
        window.blit(self.image, (self.x, self.y))  # Рисуємо танк на екрані гри

    def rotate_to(self, angle):
        # Повертаємо панцер до заданого кута
        rotate = (360 - self.angle + angle)
        self.angle = angle
        self.image = pygame.transform.rotate(self.image, rotate)  # Повертаємо зображення танка

    def strike(self):
        # Здійснюємо постріл
        if self.bullet.count == 0:  # Якщо куля не рухається
            self.bullet.x = self.x + STEP / 2 - 10  # Позиціюємо кулю по центру танка
            self.bullet.y = self.y + STEP / 2 - 10
            self.bullet.count = 50  # Встановлюємо лічильник руху кулі
            self.bullet.direction = self.angle  # Задаємо напрямок руху кулі відповідно до кута танка



class Player(Panzar):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load(os.path.join(PATH, 'images/panzer.png'))  
        self.image = pygame.transform.scale(self.image, (STEP, STEP))  # Змінюємо розмір зображення панцера

    def move(self):
        keys = pygame.key.get_pressed()  # Отримуємо стан натисканих клавіш
        if keys[pygame.K_w]:  # Якщо натиснута клавіша "вгору"
            if self.pos[1] > 0 and map[self.pos[1] - 1][self.pos[0]] == 0:  # Перевіряємо можливість руху вгору
                map[self.pos[1]][self.pos[0]] = 0  # Звільняємо попередню позицію гравця на карті
                self.y -= STEP  # Рухаємо гравця вгору на STEP пікселів
                self.pos[1] -= 1  # Змінюємо позицію гравця на карті
                map[self.pos[1]][self.pos[0]] = 1  # Позначаємо нову позицію гравця на карті
            self.rotate_to(0)  # Повертаємо гравця в напрямку "вгору"
        elif keys[pygame.K_s]:  # Якщо натиснута клавіша "вниз"
            if self.pos[1] < len(map) - 1 and map[self.pos[1] + 1][self.pos[0]] == 0:  # Перевіряємо можливість руху вниз
                map[self.pos[1]][self.pos[0]] = 0  # Звільняємо попередню позицію гравця на карті
                self.y += STEP  # Рухаємо гравця вниз на STEP пікселів
                self.pos[1] += 1  # Змінюємо позицію гравця на карті
                map[self.pos[1]][self.pos[0]] = 1  # Позначаємо нову позицію гравця на карті
            self.rotate_to(180)  # Повертаємо гравця в напрямку "вниз"
        elif keys[pygame.K_a]:  # Якщо натиснута клавіша "вліво"
            if self.pos[0] > 0 and map[self.pos[1]][self.pos[0] - 1] == 0:  # Перевіряємо можливість руху вліво
                map[self.pos[1]][self.pos[0]] = 0  # Звільняємо попередню позицію гравця на карті
                self.x -= STEP  # Рухаємо гравця вліво на STEP пікселів
                self.pos[0] -= 1  # Змінюємо позицію гравця на карті
                map[self.pos[1]][self.pos[0]] = 1  # Позначаємо нову позицію гравця на карті
            self.rotate_to(90)  # Повертаємо гравця в напрямку "вліво"
        elif keys[pygame.K_d]:  # Якщо натиснута клавіша "вправо"
            if self.pos[0] < len(map[0]) - 1 and map[self.pos[1]][self.pos[0] + 1] == 0:  # Перевіряємо можливість руху вправо
                map[self.pos[1]][self.pos[0]] = 0  # Звільняємо попередню позицію гравця на карті
                self.x += STEP  # Рухаємо гравця вправо на STEP пікселів
                self.pos[0] += 1  # Змінюємо позицію гравця на карті
                map[self.pos[1]][self.pos[0]] = 1  # Позначаємо нову позицію гравця на карті
            self.rotate_to(270)  # Повертаємо гравця в напрямку "вправо"
        elif keys[pygame.K_c]:  # Якщо натиснута клавіша "c"
            self.strike()  # Викликаємо метод для здійснення пострілу


class Player2(Panzar):
    def __init__(self, x, y):
        super().__init__(x, y)  #Викликаємо конструктор батьківського класу з параметрами x і y
        self.image = pygame.image.load(os.path.join(PATH, 'images/enemy.png'))  
        self.image = pygame.transform.scale(self.image, (STEP, STEP))  # Змінюємо розмір зображення 

    def move(self):
        keys = pygame.key.get_pressed()  # Отримуємо стан натиснених клавіш
        if keys[pygame.K_UP]:  # Якщо натиснута клавіша "вгору"
            if self.pos[1] > 0 and map[self.pos[1] - 1][self.pos[0]] == 0:  # Перевіряємо можливість руху вгору
                map[self.pos[1]][self.pos[0]] = 0  # Звільняємо попередню позицію гравця на карті
                self.y -= STEP  # Рухаємо гравця вгору на STEP пікселів
                self.pos[1] -= 1  # Змінюємо позицію гравця на карті
                map[self.pos[1]][self.pos[0]] = 2  # Позначаємо нову позицію гравця на карті 
            self.rotate_to(0)  # Повертаємо гравця в напрямку "вгору"
        elif keys[pygame.K_DOWN]:  # Якщо натиснута клавіша "вниз"
            if self.pos[1] < len(map) - 1 and map[self.pos[1] + 1][self.pos[0]] == 0:  # Перевіряємо можливість руху вниз
                map[self.pos[1]][self.pos[0]] = 0  # Звільняємо попередню позицію гравця на карті
                self.y += STEP  # Рухаємо гравця вниз на STEP пікселів
                self.pos[1] += 1  # Змінюємо позицію гравця на карті
                map[self.pos[1]][self.pos[0]] = 2  # Позначаємо нову позицію гравця на карті 
            self.rotate_to(180)  # Повертаємо гравця в напрямку "вниз"
        elif keys[pygame.K_LEFT]:  # Якщо натиснута клавіша "вліво"
            if self.pos[0] > 0 and map[self.pos[1]][self.pos[0] - 1] == 0:  # Перевіряємо можливість руху вліво
                map[self.pos[1]][self.pos[0]] = 0  # Звільняємо попередню позицію гравця на карті
                self.x -= STEP  # Рухаємо гравця вліво на STEP пікселів
                self.pos[0] -= 1  # Змінюємо позицію гравця на карті
                map[self.pos[1]][self.pos[0]] = 2  # Позначаємо нову позицію гравця на карті 
            self.rotate_to(90)  # Повертаємо гравця в напрямку "вліво"
        elif keys[pygame.K_RIGHT]:  # Якщо натиснута клавіша "вправо"
            if self.pos[0] < len(map[0]) - 1 and map[self.pos[1]][self.pos[0] + 1] == 0:  # Перевіряємо можливість руху вправо
                map[self.pos[1]][self.pos[0]] = 0  # Звільняємо попередню позицію гравця на карті
                self.x += STEP  # Рухаємо гравця вправо на STEP пікселів
                self.pos[0] += 1  # Змінюємо позицію гравця на карті
                map[self.pos[1]][self.pos[0]] = 2  # Позначаємо нову позицію гравця на карті 
            self.rotate_to(270)  # Повертаємо гравця в напрямку "вправо"
        elif keys[pygame.K_SPACE]:  # Якщо натиснута клавіша "Space"
            self.strike()  # Викликаємо метод для здійснення пострілу



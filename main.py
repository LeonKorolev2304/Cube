import pygame
import random
import sys
import os
import math
# Цели Колизия пуль
x_pos = 0
y_pos = 0
step = 10
pos_x = 900
pos_y = 100
clock = pygame.time.Clock()
sp = []
pygame.init()
size = width, height = 800, 400
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()

def load_image(name, colorkey=None):

    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

class Enemy(pygame.sprite.Sprite):
    image = load_image("2F3136.png")
    def __init__(self, x=0, y=0, *group):
        self.step = 5
        self.size = self.image.get_size()[0]
        self.y = y
        self.x = x
        self.hp = 3
        self.last = self.x, self.y
        super().__init__(*group)
        self.image = Enemy.image
        self.rect = self.image.get_rect()
    def update(self, *args, **kwargs):
        self.rect.x = self.x - self.size / 2 - x_pos
        self.rect.y = self.y - self.size / 2 - y_pos

        v = (((200 - self.y + y_pos) ** 2 + (self.x - 400 - x_pos) ** 2) ** 0.5)
        cos = (self.x - 400 - x_pos) / v
        sin = (200 - self.y + y_pos) / v
        pygame.draw.lines(screen, color='blue', closed=True, points=((self.x - x_pos, self.y - y_pos), (400, 200)))
        self.x = self.x - cos * self.step
        self.y = self.y + sin * self.step
        if pygame.sprite.spritecollide(self, bullet_sprites, True):
            self.hp -= 1
            print(self.hp)
        if self.hp == 0:
            enemy_sprites.remove(self)

#        v = (((200 - self.y + y_pos) ** 2 + (self.x - 400 - x_pos) ** 2) ** 0.5)
#        cos = (self.x - 400 - x_pos) / v
#        sin = (200 - self.y + y_pos) / v
# более плавное движение. ускорение чем дальше, чем ближе замедление
# pygame.draw.lines(screen, color='blue', closed=True, points=((self.x - x_pos, self.y - y_pos), (400, 200)))

#Можно сделать наследуемый класс Bullet, Laser и т.д?
class Bullet_type_1(pygame.sprite.Sprite):
    image = load_image("bullet.png")
    def __init__(self, x=400, y=200, *group):
        self.step = 5
        self.size = self.image.get_rect()[0]
        super().__init__(*group)
        self.image = Bullet_type_1.image
        self.rect = self.image.get_rect()
        self.x, self.y = x + x_pos, y + y_pos
#vector settings
        self.mcoord = pygame.mouse.get_pos()
        v = (((self.mcoord[1] - 200) ** 2 + (self.mcoord[0] - 400) ** 2) ** 0.5)
        cos = (self.mcoord[0] - 400) / v
        sin = (self.mcoord[1] - 200) / v
        self.vx = cos * step
        self.vy = sin * step


    def update(self, *args, **kwargs):
        self.rect.x = self.x - self.size - x_pos
        self.rect.y = self.y - self.size - y_pos
        self.x += self.vx
        self.y += self.vy
        pygame.draw.lines(screen, color='green', closed=True, points=((self.x - x_pos, self.y - y_pos), (400, 200)))


class Player():
    def __init__(self):
        pass

    def bullet_spawn(self, type=Bullet_type_1):
        type(400, 200, bullet_sprites)

class Gamerulers():
    def __init__(self):
        pass

    def spawn(self, x):
        for i in range(x):
            Enemy(800, (random.randrange(0, 400)), enemy_sprites)
            c = 0
            if c == 1:
                pass
            if c == 2:
                pass
            if c == 3:
                pass
            if c == 4:
                pass


if __name__ == '__main__':
    running = True

    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 1000)

    while running:
        clock.tick(30)
        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, (255, 0, 0), (400, 200), 20)

        # внутри игрового цикла ещё один цикл
        # приема и обработки сообщений
        for event in pygame.event.get():
       #     if event != []:
                #print(event.dict)
                #print(pygame.key.get_pressed()[119])
            if pygame.key.get_focused() and event.type == pygame.TEXTINPUT:
                if pygame.key.get_pressed()[119]:
                    y_pos -= step
                if pygame.key.get_pressed()[100]:
                    x_pos += step
                if pygame.key.get_pressed()[97]:
                    x_pos -= step
                if pygame.key.get_pressed()[115]:
                    y_pos += step
            if event.type == MYEVENTTYPE:
                Gamerulers().spawn(1)
                Player().bullet_spawn()

            # при закрытии окна
            if event.type == pygame.QUIT:
                running = False

        enemy_sprites.update()
        bullet_sprites.update()
        all_sprites.draw(screen)
        enemy_sprites.draw(screen)
        bullet_sprites.draw(screen)

    #короче когда мы пулькой попадаем то не удаляется из all sprites так что пока что оно класс пулек и врагов не принадлежит all sprites

        # отрисовка и изменение свойств объектов
        # ...

        # обновление экрана
        pygame.display.flip()
    pygame.quit()



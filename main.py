import pygame
import random
import sys
import os
import threading
import math
from PIL import Image
from PIL import ImageGrab, ImageOps
from tools import load_image, start_screen



x_pos = 0
y_pos = 0
step = 10
pos_x = 900
pos_y = 100
clock = pygame.time.Clock()
sp = []
pygame.init()
size = width, height = 1920, 1080
screen = pygame.display.set_mode((1920, 1080))
all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()
Player_sprite = pygame.sprite.Group()
Cards_sprite = pygame.sprite.Group()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        self.damagetake = threading.Timer(0.3, self.__class__.hp_change, args=(self,))
        im = ImageOps.grayscale(Image.open(f"data/{self.__class__.__name__}.png"))
        im.save(f"data/{self.__class__.__name__}(1).png")
        print(self.__class__.__name__.title())
        self.image = load_image(f"{self.__class__.__name__}.png")
        self.step = 5
        self.size = self.image.get_size()[0]
        self.y = y
        self.x = x
        self.hp = 3
        self.lasthp = self.hp
        super().__init__(enemy_sprites)
        self.rect = self.image.get_rect()
        self.damagemoment = True
        self.ex = 3
    def update(self, *args, **kwargs):
        self.rect.x = self.x - self.size / 2 - x_pos
        self.rect.y = self.y - self.size / 2 - y_pos
        v = (((screen.get_size()[1] / 2 - self.y + y_pos) ** 2 + (self.x - screen.get_size()[0] / 2 - x_pos) ** 2) ** 0.5)
        cos = (self.x - (screen.get_size()[0] / 2) - x_pos) / v
        sin = (screen.get_size()[1] / 2 - self.y + y_pos) / v
        self.x = self.x - cos * self.step
        self.y = self.y + sin * self.step
        if self.hp <= 0:
            exp.update_ex(self.ex)
            enemy_sprites.remove(self)

        if self.hp != self.lasthp and not self.damagetake.is_alive():
            self.lasthp = self.hp
            self.image = load_image(f'{self.__class__.__name__}(1).png')
            self.damagetake.start()


    def hp_change(self):
        self.image = load_image(f'{self.__class__.__name__}.png')
        self.damagetake = threading.Timer(0.3, self.__class__.hp_change, args=(self,))


#Сделать индикатор получения урона? Типо моргания белым спрайтом
class Enemy_distant(Enemy):
    image = load_image("enemy_distant.png")

    def __init__(self, x, y):
        super().__init__(x, y)
        self.distance = 200
        self.timer = 2.0
        self.thread = threading.Timer(self.timer, self.__class__.wait_time, args=(self, ))

    def update(self, *args, **kwargs):
        self.rect.x = self.x - self.size / 2 - x_pos
        self.rect.y = self.y - self.size / 2 - y_pos
        v = (((screen.get_size()[1] / 2 - self.y + y_pos) ** 2 + (self.x - screen.get_size()[0] / 2 - x_pos) ** 2) ** 0.5)
        cos = (self.x - screen.get_size()[0] / 2 - x_pos) / v
        sin = (screen.get_size()[1] / 2 - self.y + y_pos) / v
        if v >= self.distance:
            self.x = self.x - cos * self.step
            self.y = self.y + sin * self.step
        else:
            if not self.thread.is_alive():
                self.thread = threading.Timer(self.timer, Enemy_distant.wait_time, args=(self,))
                self.thread.start()
        if self.hp <= 0:
            enemy_sprites.remove(self)


    def wait_time(self):
        self.spawn()

    def spawn(self):
        Enemy_bullet(self.rect.x, self.rect.y, enemy_sprites)


#нужно еще сделать систему в которой обьекты удаляются если находятся слишком далеко
#нужно еще впредь понимать что в итоге свойста всех этих пуль будут засовываться в Player (список или что то типо того)
#Можно сделать дебафф - появление новых врагов это решит мою проблему со скупостью всего


#короче сдесть нужно сделать изменение спрайта когда оно входит в avoid типо полупрозрачным или что то типо того
#Cуть этого врага в том что иногда он перестает получать урон на время
class Enemy_avoid(Enemy):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.timeavoid = 4.0
        self.thread = threading.Timer(self.timeavoid, Enemy_avoid.enter_avoid, args=(self, ))
        self.thread.start()

    def update(self, *args, **kwargs):
        super().update()

    def enter_avoid(self):
        self.damagemoment = False
        self.thread = threading.Timer(self.timeavoid, Enemy_avoid.leave_avoid, args=(self,))
        self.thread.start()

    def leave_avoid(self):
        self.damagemoment = True
        self.thread = threading.Timer(self.timeavoid, Enemy_avoid.enter_avoid, args=(self,))
        self.thread.start()


# Враг который спавнит препятвия. Они условно обозначивают зону появления а только потом домажат
class Enemy_Waller(Enemy_distant):
    image = load_image("background_wall.png")
    def __init__(self, x, y):
        super().__init__(x, y)
        self.distance = 300
        self.timer = 5.0

    def spawn(self):
        Enemy_wall(random.randint(0, screen.get_size()[0] - self.size) + x_pos, random.randint(0, screen.get_size()[1] - self.size) + y_pos, bullet_sprites)

    def wait_time(self):
        self.spawn()

#Враг который двигается как змейка?
#Сделать какое то визуальное обозначение. Например если враг подобрался относительно близко для атаки его углы меняют цвет



#        v = (((200 - self.y + y_pos) ** 2 + (self.x - 400 - x_pos) ** 2) ** 0.5)
#        cos = (self.x - 400 - x_pos) / v
#        sin = (200 - self.y + y_pos) / v
# более плавное движение. ускорение чем дальше, чем ближе замедление
# pygame.draw.lines(screen, color='blue', closed=True, points=((self.x - x_pos, self.y - y_pos), (400, 200)))




#Можно сделать наследуемый класс Bullet, Laser и т.д?
#Добавим пуле промежуток времени через который она может наносить урон
#сделать класс просто пуль? какая разница кто чего дамажит?


class Bullet_type_standart(pygame.sprite.Sprite):
    def __init__(self, x=screen.get_size()[0] / 2, y=screen.get_size()[1] / 2, lvl=1):
        #условно уровень 1
        self.step = 5
        self.damage = 1

        #лвл прокачки данной способности
        self.lvl = lvl
        self.image = load_image(f"{self.__class__.__name__}.png")
        self.size = self.image.get_rect()[0]
        super().__init__(bullet_sprites)
        self.rect = self.image.get_rect()

        self.x, self.y = x + x_pos, y + y_pos

        self.rect.y = self.y - self.size - y_pos
        self.rect.x = self.x - self.size - x_pos
#vector settings
        self.mcoord = pygame.mouse.get_pos()
        v = (((self.mcoord[1] - screen.get_size()[1] / 2) ** 2 + (self.mcoord[0] - screen.get_size()[0] / 2) ** 2) ** 0.5)
        cos = (self.mcoord[0] - screen.get_size()[0] / 2) / v
        sin = (self.mcoord[1] - screen.get_size()[1] / 2) / v
        self.vx = cos * step
        self.vy = sin * step
        #тут нужно еще подумать это как таймер перед наложением? стоит ли это вообще использовать?
        self.start_timer = 1


        #тут будут определятся статы по лвл
        if self.lvl >= 2:
            self.step = 7.5
            #start_timer должен быть скоростью использования наложения
            self.start_timer = 0.75


    def wait_time(self):
        self.damagemoment = True
        self.damage = 2


    def update(self,d=enemy_sprites, *args, **kwargs):
        detected = pygame.sprite.spritecollideany(self, d)

        self.rect.x = self.x - self.size - x_pos
        self.rect.y = self.y - self.size - y_pos
        self.x += self.vx
        self.y += self.vy

        if detected != None and detected.damagemoment:
            detected.hp -= self.damage
            bullet_sprites.remove(self)
            #возможно сделать сдесь скорость наложение скилов

        if self.lvl == 3:
            pass
            #нужно сделать отскок от краев



#нужна доп настройка чтобы целилось в центр желательно через size
#нужно исправить что оно иногда появляется в верху экрана? Т.е скорее всего отрисовывается раньше чем надо
#Попробовать все в будущем с помощью super и класс пуль реализовать
class Enemy_bullet(pygame.sprite.Sprite):
    image = load_image("enemy_distant.png")
    def __init__(self, x=screen.get_size()[0] / 2, y=screen.get_size()[1] / 2):

        angle_in_radians = math.atan2(y - screen.get_size()[1] / 2, x - screen.get_size()[0] / 2)
        angle = angle_in_radians * 180 / math.pi
        #короче у меня не получилось сделать так чтобы оно поворачивалось к игроку но чет пошло не так ну и хрен с ним
        self.image = pygame.transform.rotate(self.__class__.image, angle)
        self.rect = self.image.get_rect()
        self.step = 5
        self.size = self.image.get_rect()[0]
        super().__init__(bullet_sprites)
        self.rect = self.image.get_rect(center=(self.size/ 2, self.size / 2))
        self.x, self.y = x + x_pos, y + y_pos
        # vector settings
        self.mcoord = x, y
        v = (((self.mcoord[1] - (screen.get_size()[1] / 2 - MainPerson.rect.size[1] / 2)) ** 2 + (self.mcoord[0] - (400 - MainPerson.rect.size[0] / 2)) ** 2) ** 0.5)
        cos = (self.mcoord[0] - (screen.get_size()[0] / 2 - MainPerson.rect.size[0] / 2)) / v
        sin = (self.mcoord[1] - (screen.get_size()[1] / 2 - MainPerson.rect.size[1] / 2)) / v
        self.vx = cos * step
        self.vy = sin * step

    def update(self,d=Player_sprite, *args, **kwargs):
        super(Bullet_type_standart).update(self, d)


class Bullet_through(Bullet_type_standart):
    def __init__(self, lvl=1):
        super().__init__()
        self.thread = threading.Timer(0.5, Bullet_type_standart.wait_time, args=self)

        self.timedamage = 2
        #timedamage не используется
        self.damagemoment = True
    def update(self, *args, **kwargs):
        detected = pygame.sprite.spritecollideany(self, enemy_sprites)
        self.rect.x = self.x - self.size - x_pos
        self.rect.y = self.y - self.size - y_pos
        self.x += self.vx
        self.y += self.vy

        if detected != None and self.damagemoment == True and detected.damagemoment:
            detected.hp -= 1
            self.damagemoment = False

        if self.damagemoment == False and not self.thread.is_alive():
            self.thread = threading.Timer(0.5, Bullet_type_standart.wait_time, args=(self, ))
            self.thread.start()

# сделать може этот класс наследуемым т.к это будет относительно статичным обьектом
#сделать чтоб сначала расширялась а потом уменьшалась
#вообще стоит сделать всего 6-7 типов снарядов но добавить кучу механик. Например у проникающей пули отскок от краев экрана
#Нужно все классы которые к игроку переснести вверх
class Wall(pygame.sprite.Sprite):

    def __init__(self, x=0, y=0, lvl=1):
        self.img = load_image("wall_not_activate.png")
        #если не лень сделать общую внешнюю функцию которая просто будет менять значения с true => False или наооборот
        self.thread = threading.Timer(0.2, self.__class__.wait_time, args=(self, ))
        self.delit = threading.Timer(4.0, self.__class__.dellit, args=(self,))
        self.delit.start()
        self.damage = 1
        self.damagemoment = True

        self.image = self.img
        self.scale = 0.3
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] * self.scale, self.image.get_size()[1] * self.scale))
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()[0]
        self.mask = pygame.mask.from_surface(self.image)
        super().__init__(bullet_sprites)
        self.rect.x = random.randint(0, screen.get_size()[0] - self.size) + x_pos
        self.rect.y = random.randint(0, screen.get_size()[1] - self.size) + y_pos
        self.pos1 = self.rect.x
        self.pos2 = self.rect.y

        if lvl == 0:
            print('2')
            self.rect.x = x
            self.rect.y = y
            self.pos2 = self.rect.y
            self.pos1 = self.rect.x


        self.lastpos = [0, 0]

        if lvl >= 2:
            self.delit = threading.Timer(7.0, self.__class__.dellit, args=(self,))
            self.damage = 2
    def update(self, d=enemy_sprites, *args, **kwargs):
        detected = pygame.sprite.spritecollideany(self, d)
        if [x_pos, y_pos] != self.lastpos:
            Wall.poschange(self, self.lastpos[0] - x_pos, self.lastpos[1] - y_pos)

        if detected != None and self.damagemoment == True:
            if not pygame.sprite.collide_mask(self, detected):
                detected.hp -= self.damage
                self.damagemoment = False
            else:
                pass
        if self.damagemoment == False and not self.thread.is_alive():
            self.thread = threading.Timer(0.5, self.__class__.wait_time, args=(self, ))
            self.thread.start()

        if self.scale <= 1:
            self.image = pygame.transform.scale(self.img, (self.img.get_size()[0] * (self.scale), self.img.get_size()[1] * (self.scale)))
            self.rect = self.image.get_rect()
            self.rect.x = self.pos1 - x_pos
            self.rect.y = self.pos2 - y_pos
            self.scale += 0.1
        else:
            self.image = load_image('wall_activate.png')
        self.lastpos = [x_pos, y_pos]

    def spawn(self):
        self.rect.x = random.randint(screen.get_size()[0] - self.size)
        self.rect.y = random.randint(screen.get_size()[1] - self.size)

    def poschange(self, x=0, y=0):
        self.rect.x += x
        self.rect.y += y

    def wait_time(self):
        self.timedamage = True

    def dellit(self):
        bullet_sprites.remove(self)

class Enemy_wall(Wall):
    image = load_image("background_wall.png")
    def __init__(self, x, y):
        super().__init__(x, y)
        self.active = False
        self.timer = 5.0
        self.threa = threading.Timer(self.timer, self.__class__.activate, args=(self, ))
        self.threa.start()
        self.damagemoment = False
    def activate(self):
        self.active = True
        self.damagemoment = True
        #Тут появляется ошибка когда мы завершаем прогу т.к она уже закрылась а функция в отложенном запуске
        self.image=load_image("active_wall.png")

    def update(self, d=Player_sprite, *args, **kwargs):
        detected = pygame.sprite.spritecollideany(self, d)
        if [x_pos, y_pos] != self.lastpos:
            if x_pos != self.lastpos[0] and y_pos == self.lastpos[1]:
                Wall.poschange(self, x=self.lastpos[0] - x_pos)
            elif y_pos != self.lastpos[1] and x_pos == self.lastpos[0]:
                Wall.poschange(self, y=self.lastpos[1] - y_pos)
            else:
                Wall.poschange(self, self.lastpos[0] - x_pos, self.lastpos[1] - y_pos)
        if self.active:
            if detected != None and self.damagemoment == True:
                if not pygame.sprite.collide_mask(self, detected):
                    detected.hp -= 1
                    self.damagemoment = False
            if self.damagemoment == False and not self.thread.is_alive():
                self.thread = threading.Timer(0.5, Bullet_type_standart.wait_time, args=(self,))
                self.thread.start()

        self.lastpos = [x_pos, y_pos]


class remote_bullet(Bullet_type_standart):
    def __init__(self, lvl=3):
        self.lastpos = [0, 0]
        super().__init__()
        self.mx, self.my = pygame.mouse.get_pos()
        self.img = load_image(f'{self.__class__.__name__}.png')
        rel_x, rel_y = self.mx - self.x, self.my - self.y
        self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

        self.image, self.rect = self.rot_center(self.img, self.angle, self.x, self.y)

        if lvl >= 2:
            self.damage = 2
            #время наложения
        if lvl == 3:
            pass
        self.y = screen.get_size()[1] / 2 + y_pos
        self.x = screen.get_size()[0] / 2 + x_pos


    def update(self, *args, **kwargs):
        if [x_pos, y_pos] != self.lastpos:
            self.poschange((self.lastpos[0] - x_pos), (self.lastpos[1] - y_pos))
            self.lastpos = [x_pos, y_pos]
        detected = pygame.sprite.spritecollideany(self, enemy_sprites)
        self.mx, self.my = pygame.mouse.get_pos()
        rel_x, rel_y = self.mx - self.x, self.my - self.y

        #self.image = pygame.transform.rotate(self.image, (180 / math.pi) * -math.atan2(rel_y, rel_x) - self.angle)
        #self.rect = self.image.get_rect()
        #self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)


        v = (((self.my - self.y) ** 2 + (self.x - self.mx) ** 2) ** 0.5)
        cos = (self.x - self.mx) / v
        sin = (self.my - self.y) / v
        self.x = (self.x - cos * self.step)
        self.y = (self.y + sin * self.step)
        self.image, self.rect = self.rot_center(load_image(f'{self.__class__.__name__}.png'), (180 / math.pi) * -math.atan2(rel_y, rel_x) - self.angle,
                                                self.x, self.y)

        if detected != None and detected.damagemoment:
            detected.hp -= self.damage
            bullet_sprites.remove(self)
            if self.lvl == 3:
                Wall(self.x - 50, self.y - 50, lvl=0)
    def rot_center(self, z, angle, x, y):
        rotated_image = pygame.transform.rotate(z, angle)
        new_rect = rotated_image.get_rect(center=z.get_rect(center=(x, y)).center)

        return rotated_image, new_rect
#
    def poschange(self, x=0, y=0):
        self.x += x
        self.y += y


# будет крутиться вокруг игрока изменяется колличество крутящихся штук урон
class circle(pygame.sprite.Sprite):
    def __init__(self, lvl=1):
        self.image = load_image('active_wall.png')
        self.rect = self.image.get_rect()
        self.count = 1
        super().__init__(bullet_sprites)
        #x = x0 + r⋅cos δ
        #y = y0 + r⋅sin δ
        self.r = 200
        self.angle = 0
        self.rect.x = screen.get_size()[0] / 2 + (self.r * math.cos(self.angle))
        self.rect.y = screen.get_size()[1] / 2 + (self.r * math.sin(self.angle))
        self.thread = threading.Timer(0.1, self.__class__.wait_time, args=(self,))
    def update(self, *args, **kwargs):
        if not self.thread.is_alive():
            self.thread = threading.Timer(0.0, self.__class__.wait_time, args=(self,))
            self.thread.start()

        self.rect.x = (screen.get_size()[0] / 2 - 50) + (self.r * math.cos(self.angle))
        self.rect.y = (screen.get_size()[1] / 2 - 50) + (self.r * math.sin(self.angle))

    def wait_time(self):
        self.angle += 0.1

class Tunder(pygame.sprite.Sprite):
    def __init__(self):
        self.count = 3
        self.x, self.y = screen.get_size()[0] / 2, screen.get_size()[1] / 2

    def ray_l(self, object):
        v = (((self.y - object.y) ** 2 + (self.x - object.x) ** 2) ** 0.5)
        cos = (self.x - (screen.get_size()[0] / 2)) / v
        sin = (screen.get_size()[1] / 2 - self.y + y_pos) / v
        pass


#вокруг кубика по окружности
#any([pygame.sprite.mask(self, i) for i in enemy_sprites.sprites])
#Можно попробовать использовать для проверки перечения по группе спрайтов а не по одному

class floor_stuff(pygame.sprite.Sprite):
    def __init__(self):
        # будет рандомно раз в 2 - 3 секунды либо кусочек опыта либо кусочек жизни
        if random.choice([True, False]):
            self.image = load_image(f'{self.__class__.__name__}_1.png')
            self.state = 1
        else:
            self.state = 2
            self.image = load_image(f'{self.__class__.__name__}_2.png')
        self.rect = self.image.get_rect()
        super().__init__(bullet_sprites)
        self.size = self.image.get_size()[0]
        self.rect.x = random.randint(0, screen.get_size()[0] - self.size) + x_pos
        self.rect.y = random.randint(0, screen.get_size()[1] - self.size) + y_pos
        self.pos1 = self.rect.x
        self.pos2 = self.rect.y
        self.lastpos = [0, 0]


    def update(self, *args, **kwargs):
        detected = pygame.sprite.spritecollideany(self, Player_sprite)
        if [x_pos, y_pos] != self.lastpos:
            self.poschange(self.lastpos[0] - x_pos, self.lastpos[1] - y_pos)

        if detected != None:
            if self.state == 2:
                MainPerson.hp += 1
            else:
                exp.update_ex(1)
            bullet_sprites.remove(self)
        self.lastpos = [x_pos, y_pos]

    def poschange(self, x=0, y=0):
        self.rect.x += x
        self.rect.y += y
    

class ex(pygame.sprite.Sprite):
    image = load_image('ex.png')

    def __init__(self):
        self.size = self.image.get_rect()[0]
        super().__init__(all_sprites)
        self.image = self.__class__.image
        self.rect = self.image.get_rect()
        self.x, self.y = 0, 0
        self.progress = 23
        # функция рассчета опыта (x * 10) ^ 1,4
        self.current_maximum_value = (1 * 10) ** 1.4
        self.lvl = 1
        self.update_ex(0)

    def update_ex(self, exp):
        self.progress += exp
        if self.progress >= self.current_maximum_value:
            self.progress = self.progress - self.current_maximum_value
            self.lvl += 1
            self.current_maximum_value = (self.lvl * 10) * 1.4
            Game().choose()
        self.image = pygame.transform.scale(self.image, (self.progress / self.current_maximum_value * screen.get_size()[0], 10))


#Можно добавить эффекты например раз в 10 секунд бессмертие или что то подобное
class Player(pygame.sprite.Sprite):
    global type_store_player
    image = load_image("ff.png")
    def __init__(self):
        self.hp = 3
        super().__init__(Player_sprite)
        self.image = Player.image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = screen.get_size()[0] / 2 - self.image.get_size()[0] / 2
        self.rect.y = screen.get_size()[1] / 2 - self.image.get_size()[0] / 2

    def bullet_spawn(self):
        for i in range(len(type_store_player)):
            #короче от лвл скейлится как и уровень способности так и колличество
            self.thread = threading.Timer(0 * (i), self.__class__.waiter, args=(self, i, ))
            self.thread.start()
    def waiter(self, i):
        type_store_player[i](lvl=type_store_player.count(type_store_player[i]))
        self.thread = threading.Timer(0 * (i), self.__class__.waiter, args=(self, i,))
    def update(self, *args, **kwargs):
        #это должно быть у класса враги
        font = pygame.font.Font(None, 100)
        text = font.render(f"{self.hp} ОЗ", True, (255, 255, 255))
        screen.blit(text, (1750, 100))
        if self.hp > 3:
            self.hp = 3
        if pygame.sprite.spritecollide(self, enemy_sprites, True):
            self.hp -= 1
        if self.hp == 0:
            pass

            #финальный экран


class Game():
    def __init__(self):

        self.create_cards = 3
#добавить штуку типо type как в person
    def spawn(self, x):
        for i in range(x):
            Enemy(screen.get_size()[0], (random.randrange(0, screen.get_size()[1])))
            floor_stuff()
            c = 0
            if c == 1:
                pass
            if c == 2:
                pass
            if c == 3:
                pass
            if c == 4:
                pass

    def choose(self):
        global stop_time
        random.shuffle(Сard_storage)
        c = Сard_storage
        for i in c[:self.create_cards]:
            print(i[0], i[1])
            Cards(i[0], i[1], Сard_storage.index(i) + 1, self.create_cards)
        stop_time = True



#Короче класс будет устроен так. Я определю карточки и на картинке будет текст собственно у каждой карточки пропишу свойства и все можно будет при выборе сразу передать эти свойства выше
class Cards(pygame.sprite.Sprite):
    #временная заглушка потом к каждой карточке будет своя картинка с текстом
    def __init__(self, img, type, pos, count):
        self.count = count
        self.pos = pos
        self.img = load_image(img)
        self.type = type
        super().__init__(Cards_sprite)
        self.image = load_image(img)
        self.rect = self.image.get_rect()
        self.step = (screen.get_size()[0] - self.rect.size[0] * count) / (count + 1)
        self.rect.x = (self.step * pos) + (self.rect.size[0] * (pos - 1))
        self.rect.y = 25
        self.stop_time = False

        #свойства
        #random из списка

    def update(self, *args):
        if args[0].type == pygame.MOUSEMOTION:
            if args and self.rect.collidepoint(args[0].pos):
                self.image = pygame.transform.scale(self.image, (self.img.get_size()[0] * 1.15, self.img.get_size()[1] * 1.15))
                self.rect = self.image.get_rect()
                self.step = (screen.get_size()[0] - self.rect.size[0] * self.count) / (self.count + 1)
                self.rect.x = (self.step * self.pos) + (self.rect.size[0] * (self.pos - 1))
                self.rect.y = 25

            else:
                self.image = self.img
                self.rect = self.image.get_rect()
                self.step = (screen.get_size()[0] - self.rect.size[0] * self.count) / (self.count + 1)
                self.rect.x = (self.step * self.pos) + (self.rect.size[0] * (self.pos - 1))
                self.rect.y = 25
        if args[0].type == pygame.MOUSEBUTTONDOWN:
            if args and self.rect.collidepoint(args[0].pos):
                self.chose()

    def chose(self):
        global stop_time
        type_store_player.append(self.type)
        stop_time = False
        Cards_sprite.empty()


#cдесь будут выбираться все возможные карточки в виде(img, type) все остальное будет определятся при раздачи ролей
Сard_storage = [('card_standart_bullet.png', Bullet_type_standart),
                ('card_wall.png', Wall),
                ('card_remote_bullet.png', remote_bullet),
                ('card_bullet_through.png', Bullet_through),
                ]


#тут начальный набор старта игры
type_store_player = [remote_bullet]
#v = circle()

if __name__ == '__main__':

    exp = ex()
    running = True
    stop_time = False
    MainPerson = Player()
    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 2000)
    start_screen(screen)

    while running:
        clock.tick(30)
        screen.fill((0, 0, 0))

        # внутри игрового цикла ещё один цикл
        # приема и обработки сообщений
        for event in pygame.event.get():
       #     if event != []:
                #print(event.dict)
                #print(pygame.key.get_pressed()[119])
    #cделать это в player?
    #явно стоит переработать управление сделать более быструю отзывчивость
            if pygame.key.get_focused() and event.type == pygame.TEXTINPUT and not stop_time:
                if pygame.key.get_pressed()[119]:
                    y_pos -= step
                if pygame.key.get_pressed()[100]:
                    x_pos += step
                if pygame.key.get_pressed()[97]:
                    x_pos -= step
                if pygame.key.get_pressed()[115]:
                    y_pos += step
            if event.type == MYEVENTTYPE and not stop_time:
                Game().spawn(1)
                MainPerson.bullet_spawn()
            if stop_time:
                if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                    Cards_sprite.update(event)

            # при закрытии окна
            if event.type == pygame.QUIT:
                running = False
        if not stop_time:
            enemy_sprites.update()
            bullet_sprites.update()
            MainPerson.update()

        all_sprites.draw(screen)
        enemy_sprites.draw(screen)
        bullet_sprites.draw(screen)
        Player_sprite.draw(screen)
        if stop_time:
             Cards_sprite.draw(screen)
        pygame.display.flip()

    #короче когда мы пулькой попадаем то не удаляется из all sprites так что пока что оно класс пулек и врагов не принадлежит all sprites

        # отрисовка и изменение свойств объектов
        # ...

        # обновление экрана
    pygame.quit()

import pygame
import random
import sys
import os
import asyncio
import threading
import math
import time

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
Player_sprite = pygame.sprite.Group()

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
        super().__init__(*group)
        self.image = Enemy.image
        self.rect = self.image.get_rect()
        self.damagemoment = True
    def update(self, *args, **kwargs):
        self.rect.x = self.x - self.size / 2 - x_pos
        self.rect.y = self.y - self.size / 2 - y_pos
        v = (((200 - self.y + y_pos) ** 2 + (self.x - 400 - x_pos) ** 2) ** 0.5)
        cos = (self.x - 400 - x_pos) / v
        sin = (200 - self.y + y_pos) / v
        pygame.draw.lines(screen, color='blue', closed=True, points=((self.x - x_pos, self.y - y_pos), (400, 200)))
        self.x = self.x - cos * self.step
        self.y = self.y + sin * self.step
        if self.hp <= 0:
            enemy_sprites.remove(self)


#Сделать индикатор получения урона? Типо моргания белым спрайтом
class Enemy_distant(Enemy):
    image = load_image("enemy_distant.png")

    def __init__(self, x, y, *group):
        super().__init__(x, y, *group)
        self.distance = 200
        self.timer = 2.0
        self.thread = threading.Timer(self.timer, self.__class__.wait_time, args=self)

    def update(self, *args, **kwargs):
        self.rect.x = self.x - self.size / 2 - x_pos
        self.rect.y = self.y - self.size / 2 - y_pos
        v = (((200 - self.y + y_pos) ** 2 + (self.x - 400 - x_pos) ** 2) ** 0.5)
        cos = (self.x - 400 - x_pos) / v
        sin = (200 - self.y + y_pos) / v
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
    def __init__(self, x=0, y=0, *group):
        super().__init__(x, y, *group)
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
    def __init__(self, x, y, *group):
        super().__init__(x, y, group)
        self.distance = 300
        self.timer = 5.0

    def spawn(self):
        Enemy_wall(random.randint(0, 800 - self.size) + x_pos, random.randint(0, 400 - self.size) + y_pos, bullet_sprites)

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
    image = load_image("bullet.png")
    def __init__(self, x=400, y=200, *group):
        self.step = 5
        self.size = self.image.get_rect()[0]
        super().__init__(*group)
        self.image = self.__class__.image
        self.rect = self.image.get_rect()
        self.x, self.y = x + x_pos, y + y_pos
#vector settings
        self.mcoord = pygame.mouse.get_pos()
        v = (((self.mcoord[1] - 200) ** 2 + (self.mcoord[0] - 400) ** 2) ** 0.5)
        cos = (self.mcoord[0] - 400) / v
        sin = (self.mcoord[1] - 200) / v
        self.vx = cos * step
        self.vy = sin * step

    def wait_time(self):
        self.damagemoment = True


    def update(self,d=enemy_sprites, *args, **kwargs):
        detected = pygame.sprite.spritecollideany(self, d)

        self.rect.x = self.x - self.size - x_pos
        self.rect.y = self.y - self.size - y_pos
        self.x += self.vx
        self.y += self.vy
        pygame.draw.lines(screen, color='green', closed=True, points=((self.x - x_pos, self.y - y_pos), (400, 200)))

        if detected != None and detected.damagemoment:
            detected.hp -= 1
            bullet_sprites.remove(self)


#нужна доп настройка чтобы целилось в центр желательно через size
#нужно исправить что оно иногда появляется в верху экрана? Т.е скорее всего отрисовывается раньше чем надо
#Попробовать все в будущем с помощью super и класс пуль реализовать
class Enemy_bullet(pygame.sprite.Sprite):
    image = load_image("enemy_distant.png")
    def __init__(self, x=400, y=200, *group):

        angle_in_radians = math.atan2(y - 200, x - 400)
        angle = angle_in_radians * 180 / math.pi
        #короче у меня не получилось сделать так чтобы оно поворачивалось к игроку но чет пошло не так ну и хрен с ним
        self.image = pygame.transform.rotate(self.__class__.image, angle)
        self.rect = self.image.get_rect()
        self.step = 5
        self.size = self.image.get_rect()[0]
        super().__init__(*group)
        self.rect = self.image.get_rect()
        self.x, self.y = x + x_pos, y + y_pos
        # vector settings
        self.mcoord = x, y
        v = (((self.mcoord[1] - (200 - MainPerson.rect.size[1] / 2)) ** 2 + (self.mcoord[0] - (400 - MainPerson.rect.size[0] / 2)) ** 2) ** 0.5)
        cos = (self.mcoord[0] - (400 - MainPerson.rect.size[0] / 2)) / v
        sin = (self.mcoord[1] - (200 - MainPerson.rect.size[1] / 2)) / v
        self.vx = cos * step
        self.vy = sin * step

    def update(self,d=Player_sprite, *args, **kwargs):
        super(Bullet_type_standart).update(self, d)


class Bullet_through(Bullet_type_standart):
    def __init__(self):
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
        pygame.draw.lines(screen, color='green', closed=True, points=((self.x - x_pos, self.y - y_pos), (400, 200)))



        if detected != None and self.damagemoment == True and detected.damagemoment:
            detected.hp -= 1
            print(detected.hp)
            self.damagemoment = False

        if self.damagemoment == False and not self.thread.is_alive():
            self.thread = threading.Timer(0.5, Bullet_type_standart.wait_time, args=(self, ))
            self.thread.start()

# сделать може этот класс наследуемым т.к это будет относительно статичным обьектом
#сделать чтоб сначала расширялась а потом уменьшалась
#вообще стоит сделать всего 6-7 типов снарядов но добавить кучу механик. Например у проникающей пули отскок от краев экрана
#Нужно все классы которые к игроку переснести вверх
class Wall(pygame.sprite.Sprite):
    image = load_image("w.png")

    def __init__(self, x, y,*group):
        #если не лень сделать общую внешнюю функцию которая просто будет менять значения с true => False или наооборот
        self.thread = threading.Timer(0.5, self.__class__.wait_time, args=self)
        self.damagemoment = True

        self.size = self.image.get_size()[0]
        self.hp = 5
        super().__init__(*group)
        self.image = self.__class__.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.x = random.randint(0, 800 - self.size) + x_pos
        self.rect.y = random.randint(0, 400 - self.size) + y_pos


        self.lastpos = [0, 0]

    def update(self, d=enemy_sprites, *args, **kwargs):
        detected = pygame.sprite.spritecollideany(self, d)
        if [x_pos, y_pos] != self.lastpos:
            if x_pos != self.lastpos[0] and y_pos == self.lastpos[1]:
                Wall.poschange(self, x=self.lastpos[0] - x_pos)
            elif y_pos != self.lastpos[1] and x_pos == self.lastpos[0]:
                Wall.poschange(self, y=self.lastpos[1] - y_pos)
            else:
                Wall.poschange(self, self.lastpos[0] - x_pos, self.lastpos[1] - y_pos)

        if detected != None and self.damagemoment == True:
            if not pygame.sprite.collide_mask(self, detected):
                detected.hp -= 1
                self.damagemoment = False
            else:
                pass
        if self.damagemoment == False and not self.thread.is_alive():
            self.thread = threading.Timer(0.5, self.__class__.wait_time, args=(self, ))
            self.thread.start()

        self.lastpos = [x_pos, y_pos]

    def spawn(self):
        self.rect.x = random.randint(800 - self.size)
        self.rect.y = random.randint(400 - self.size)

    def poschange(self, x=0, y=0):
        self.rect.x += x
        self.rect.y += y

    def wait_time(self):
        self.timedamage = True


class Enemy_wall(Wall):
    image = load_image("background_wall.png")
    def __init__(self, x, y, *group):
        super().__init__(x, y, group)
        self.active = False
        self.timer = 5.0
        self.threa = threading.Timer(self.timer, self.__class__.activate, args=(self, ))
        self.threa.start()
        self.damagemoment = False
    def activate(self):
        self.active = True
        self.damagemoment = True
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
                else:
                    pass
            if self.damagemoment == False and not self.thread.is_alive():
                self.thread = threading.Timer(0.5, Bullet_type_standart.wait_time, args=(self,))
                self.thread.start()

        self.lastpos = [x_pos, y_pos]


class remote_bullet(Bullet_type_standart):
    image = load_image("bullet.png")
    #тут надо другую png поставить
    def __init__(self, x, y, *group):
        super().__init__()
        self.step = 5
        self.size = self.image.get_size()[0]
        self.y = 200
        self.x = 400
        self.hp = 3
        super().__init__(x, y, *group)
        self.image = Enemy.image
        self.rect = self.image.get_rect()
    def update(self, *args, **kwargs):
        self.rect.x = self.x - self.size / 2 - x_pos
        self.rect.y = self.y - self.size / 2 - y_pos
        self.mx, self.my = pygame.mouse.get_pos()
        v = (((self.my - self.y + y_pos) ** 2 + (self.x - self.mx - x_pos) ** 2) ** 0.5)
        cos = (self.x - self.mx - x_pos) / v
        sin = (self.my - self.y + y_pos) / v
        pygame.draw.lines(screen, color='blue', closed=True, points=((self.x - x_pos, self.y - y_pos), (400, 200)))
        self.x = self.x - cos * self.step
        self.y = self.y + sin * self.step
#



#вокруг кубика по окружности
#any([pygame.sprite.mask(self, i) for i in enemy_sprites.sprites])
#Можно попробовать использовать для проверки перечения по группе спрайтов а не по одному
class eq:
    pass


#Можно добавить эффекты например раз в 10 секунд бессмертие или что то подобное
class Player(pygame.sprite.Sprite):
    image = load_image("ff.png")
    def __init__(self, *group):
        self.hp = 3
        super().__init__(*group)
        self.image = Player.image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 400 - self.image.get_size()[0] / 2
        self.rect.y = 200 - self.image.get_size()[0] / 2

    def bullet_spawn(self, type=remote_bullet):
        type(400, 200, bullet_sprites)

    def update(self, *args, **kwargs):
        #это должно быть у класса враги
        if pygame.sprite.spritecollide(self, enemy_sprites, True):
            self.hp -= 1
        if self.hp == 0:
            pass
            #финальный экран


class Gamerulers():
    def __init__(self):
        pass
#добавить штуку типо type как в person
    def spawn(self, x):
        for i in range(x):
            Enemy_Waller(800, (random.randrange(0, 400)), enemy_sprites)
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
    MainPerson = Player(all_sprites)
    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 2000)

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
                MainPerson.bullet_spawn(Bullet_type_standart)

            # при закрытии окна
            if event.type == pygame.QUIT:
                running = False

        enemy_sprites.update()
        bullet_sprites.update()
        MainPerson.update()
        
        all_sprites.draw(screen)
        enemy_sprites.draw(screen)
        bullet_sprites.draw(screen)
        Player_sprite.draw(screen)

    #короче когда мы пулькой попадаем то не удаляется из all sprites так что пока что оно класс пулек и врагов не принадлежит all sprites

        # отрисовка и изменение свойств объектов
        # ...

        # обновление экрана
        pygame.display.flip()
    pygame.quit()

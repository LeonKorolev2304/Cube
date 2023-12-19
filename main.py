import pygame
import random
import math

x_pos = 0
y_pos = 0
step = 10
pos_x = 900
pos_y = 100
clock = pygame.time.Clock()
sp = []


class Enemy():
    def __init__(self, x=0, y=0):
        self.step = 5
        self.size = 100
        self.y = y
        self.x = x
        self.last = self.x, self.y

    def move(self):
        pygame.draw.rect(screen, color='white',
                         rect=((self.x - self.size / 2 - x_pos, self.y - self.size / 2 - y_pos), (100, 100)))
        self.last = self.x, self.y
        #нельзя давать меняться self.x и y когда они застыли Создать еще переменную для фиксации?
        #место колизии я попробую расчитывать на то что фон будет серым, а враги яркими, за счет этого при выстреле например из пули когда её цвет меняется(наложением) мы отнимаем хп
        v = (((200 - self.y + y_pos) ** 2 + (self.x - 400 - x_pos) ** 2) ** 0.5)
        cos = (self.x - 400 - x_pos) / v
        sin = (200 - self.y + y_pos) / v
        pygame.draw.lines(screen, color='blue', closed=True, points=((self.x - x_pos, self.y - y_pos), (400, 200)))
        self.x = self.x - cos * self.step
        self.y = self.y + sin * self.step
        print(self.x, self.y)

#        v = (((200 - self.y + y_pos) ** 2 + (self.x - 400 - x_pos) ** 2) ** 0.5)
#        cos = (self.x - 400 - x_pos) / v
#        sin = (200 - self.y + y_pos) / v
# более плавное движение. ускорение чем дальше, чем ближе замедление
# pygame.draw.lines(screen, color='blue', closed=True, points=((self.x - x_pos, self.y - y_pos), (400, 200)))
class Player():
    def __init__(self):
        pass
class Gamerulers():
    def __init__(self):
        pass

    def spawn(self, x):
        sp = []
        for i in range(x):
            sp.append(Enemy(800, (random.randrange(0, 400))))
            if c == 1:
                pass
            if c == 2:
                pass
            if c == 3:
                pass
            if c == 4:
                pass

        return sp


c = Enemy(500, 100)

if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)
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
                sp += (Gamerulers().spawn(1))

            # при закрытии окна
            if event.type == pygame.QUIT:
                running = False
        print(sp)
        [i.move() for i in sp]

        # отрисовка и изменение свойств объектов
        # ...

        # обновление экрана
        pygame.display.flip()
    pygame.quit()

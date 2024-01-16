import time
import threading
import pygame
import sys
import os
import sqlite3


FPS = 50
size = WIDTH, HEIGHT = 1920, 1020
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
clock = pygame.time.Clock()
#define colours
bg = (204, 102, 0)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)
btn_sprites_1 = pygame.sprite.Group()
btn_sprites_2 = pygame.sprite.Group()
font = pygame.font.SysFont('Constantia', 30)
con = sqlite3.connect("data2.sqlite")
cur = con.cursor()

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if self.rect.w <= 260:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if self.rect.collidepoint(event.pos):
                    # Toggle the active variable.
                    self.active = not self.active
                else:
                    self.active = False
                # Change the current color of the input box.
                self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        print(self.text)
                        self.text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode
                    # Re-render the text.
                    self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        if self.rect.w <= 260:
            width = max(self.rect[2], self.txt_surface.get_width()+10)
            self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
FONT = pygame.font.Font(None, 32)


class button(pygame.sprite.Sprite):
    button_col = (255, 0, 0)
    hover_col = (75, 225, 255)
    click_col = (50, 150, 255)
    text_col = black
    width = 260
    height = 70

    def __init__(self, x, y, text, type, group):
        self.x = x
        self.y = y
        self.type = type
        self.text = text
        self.image = load_image('btn.png')
        super().__init__(group)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        

    def update(self, *args):
        global clicked
        action = False
        if args != ():
            print(args)
            if args[0].type == pygame.MOUSEBUTTONDOWN:
                if args and self.rect.collidepoint(args[0].pos):
                    if self.type == 1:
                        self.play()
                    if self.type == 2:
                        self.back()
                    if self.type == 4 and input_box1.text != '':
                        con.execute(f"""INSERT INTO [table] (
                        score,
                        nickname
                    )
                    VALUES (
                        '0',
                        '{input_box1.text}'
                    );""").fetchall()

                        self.final_play()
                        con.commit()
                    if self.type == 3:
                        terminate()


        text_img = font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 25))

    def play(self):
        global hide_inpt, hide_btn_1
        hide_inpt = False
        hide_btn_1 = True
        #os.startfile('main.exe')
        #sys.exit()

    def gg(self):
        terminate()

    def final_play(self):
        pygame.quit()
        c = threading.Timer(1.0, terminate)
        c.start()
        os.startfile('main.exe')

    def back(self):
        global hide_inpt, hide_btn_1
        print(hide_inpt, hide_btn_1)
        hide_inpt = True
        hide_btn_1 = False

def terminate():
    sys.exit()


def start_screen(screen):
    intro_text = ['Правила:',
                  'Cube — игра жанра Roguelike.',
                  'Враги движутся в сторону игрока.',
                  'Игрок постоянно с определённой периодичностью стреляет в сторону курсора.',
                  'Чтобы убить врага, нужно выстрелить в него 3 раза.',
                  'При каждом убийстве шкала наверху заполняется всё больше и больше.',
                  'Когда она заполнится игроку будет доступен выбор из трёх улучшений.',
                  'Если игрок подойдёт слишком близко к врагу, то потеряет очко здоровья, а враг исчезнет.',
                  'У игрока 3 очка здоровья.']


    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return 0
        pygame.display.flip()
        clock.tick(FPS)

def records_table():
    pass


def end_screen(screen):
    intro_text = ["Таблица рекордов", "",
                  "1 -",
                  "2 -",
                  "3 -"]

    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    font = pygame.font.Font()
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return 0
        pygame.display.flip()
        clock.tick(FPS)

        screen.fill(0, 0, 0)


def main():
    global done, hide_inpt, hide_btn_1, input_box1
    hide_btn_1 = False
    hide_inpt = True
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('arial', 30)
    again = button(screen.get_size()[0] / 2 - 90, screen.get_size()[1] / 3, 'Play', type=1, group=btn_sprites_1)
    quit = button(screen.get_size()[0] / 2 - 90, (screen.get_size()[1] / 3) * 2, 'Return', type=2, group=btn_sprites_2)
    back = button(screen.get_size()[0] / 2 - 90, (screen.get_size()[1] / 3) * 2, 'Quit', type=3, group=btn_sprites_1)
    final_play = button(screen.get_size()[0] / 2 - 90, (screen.get_size()[1] / 3) * 1.5, 'Play', type=4, group=btn_sprites_2)
    input_box1 = InputBox(screen.get_size()[0] / 2 - 90, screen.get_size()[1] / 3, 260, 40)
    #input_box2 = InputBox(screen.get_size()[0] / 2 - 90, (screen.get_size()[1] / 3) * 2, 260, 70)
    input_boxes = [input_box1]
    done = False
    counter = 0
    while not done:
        screen.fill((30, 30, 30))
        for event in pygame.event.get():
            for box in input_boxes:
                box.handle_event(event)

            if event.type == pygame.QUIT:
                done = True
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN and not hide_btn_1:
                btn_sprites_1.update(event)
            if event.type == pygame.MOUSEBUTTONDOWN and hide_btn_1:
                btn_sprites_2.update(event)

        if not hide_inpt:
            for box in input_boxes:
                box.update()
                box.draw(screen)

        if not hide_btn_1:
            btn_sprites_1.draw(screen)
            btn_sprites_1.update()
        else:
            btn_sprites_2.draw(screen)
            btn_sprites_2.update()
        pygame.display.flip()

        clock.tick(30)
    pygame.quit()

main()

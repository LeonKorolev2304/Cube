import threading
import pygame
import sys
import os
import sqlite3
import time
# только кнопка вернутся
clicked = False
FPS = 50
size = WIDTH, HEIGHT = 1920, 1080
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
clock = pygame.time.Clock()
font = pygame.font.SysFont('Times New Roman', 30)
bg = (204, 102, 0)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)
btn_sprites_1 = pygame.sprite.Group()
btn_sprites_2 = pygame.sprite.Group()
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
            width = max(self.rect[2], self.txt_surface.get_width() + 10)
            self.rect.w = width

    def draw(self, sreen):
        # Blit the text.
        sreen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(sreen, self.color, self.rect, 2)


FONT = pygame.font.Font(None, 32)


class Button(pygame.sprite.Sprite):
    button_col = (255, 0, 0)
    hover_col = (75, 225, 255)
    click_col = (50, 150, 255)
    text_col = black
    width = 260
    height = 70

    def __init__(self, x, y, text, typ, group):
        self.x = x
        self.y = y
        self.typ = typ
        self.text = text
        self.image = load_image('btn.png')
        super().__init__(group)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self, *args):
        global clicked
        if args != ():
            if args[0].type == pygame.MOUSEBUTTONDOWN:
                if args and self.rect.collidepoint(args[0].pos):
                    if self.typ == 1:
                        self.play()
                    if self.typ == 2:
                        self.back()
                    if self.typ == 4 and input_box1.text != '':
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
                    if self.typ == 3:
                        terminate()
                    if self.typ == 5:
                        self.return_to_main()
        try:
            pygame.font.Font(pygame.font.match_font('verdana', 36), 4)
        except BaseException:
            pass
        #pygame.font.Font('/адрес/Arial.ttf', 36)
        text_img = font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 25))

    def play(self):
        self.text = self.text
        global hide_inpt, hide_btn_1
        hide_inpt = False
        hide_btn_1 = True

    def gg(self):
        self.text = self.text
        terminate()

    def final_play(self):
        self.text = self.text
        pygame.quit()
        c = threading.Timer(1.0, terminate)
        c.start()
        os.startfile('main.Exe')

    def back(self):
        self.text = self.text
        global hide_inpt, hide_btn_1
        hide_inpt = True
        hide_btn_1 = False

    def return_to_main(self):
        self.text = self.text
        os.startfile('testers.exe')
        time.sleep(1)
        terminate()



def records_table():
    pygame.quit()
    c = threading.Timer(1.0, terminate)
    c.start()
    # os.startfile('main.Exe')

def terminate():
    sys.exit()

def main():
    pygame.init()
    pygame.font.init()
    global done, hide_inpt, hide_btn_1, input_box1
    hide_btn_1 = False
    hide_inpt = True
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('arial', 30)
    again = Button(screen.get_size()[0] / 2 - 90, screen.get_size()[1] / 3, 'Play', typ=1, group=btn_sprites_1)
    quit = Button(screen.get_size()[0] / 2 - 90, (screen.get_size()[1] / 3) * 2, 'Return', typ=2, group=btn_sprites_2)
    back = Button(screen.get_size()[0] / 2 - 90, (screen.get_size()[1] / 3) * 2, 'Quit', typ=3, group=btn_sprites_1)
    final_play = Button(screen.get_size()[0] / 2 - 90, (screen.get_size()[1] / 3) * 1.5, 'Play', typ=4,
                        group=btn_sprites_2)
    input_box1 = InputBox(screen.get_size()[0] / 2 - 90, screen.get_size()[1] / 3, 260, 40)
    # input_box2 = InputBox(screen.get_size()[0] / 2 - 90, (screen.get_size()[1] / 3) * 2, 260, 70)
    input_boxes = [input_box1]
    done = False
    counter = 0
    while not done:
        screen.fill((30, 30, 30))
        for event in pygame.event.get():
            for box in input_boxes:
                box.handle_event(event)

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not hide_btn_1:
                btn_sprites_1.update(event)
            if event.type == pygame.MOUSEBUTTONDOWN and hide_btn_1:
                try:
                    btn_sprites_2.update(event)
                except BaseException:
                    pass

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


if __name__ == '__main__':
    pygame.init()
    try:
        main()
    except BaseException:
        pass
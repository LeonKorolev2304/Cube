import pygame
from testers import Button
import sqlite3


# Меню (Играть, таблица лидеров, выход) Если и таблицу лидеров и только кнопка вернутся
clicked = False
FPS = 50
size = WIDTH, HEIGHT = 1920, 1080
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
clock = pygame.time.Clock()
btn_sprites_2 = pygame.sprite.Group()
bg = (204, 102, 0)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)
btn_sprites_1_1 = pygame.sprite.Group()
font = pygame.font.SysFont('arial', 30)
FONT = pygame.font.Font(None, 32)
text_col = black
con = sqlite3.connect("data2.sqlite")
cur = con.cursor()
n = cur.execute(f"""SELECT MAX(id)
  FROM [table]""").fetchall()[0][0]

results = cur.execute(f"""SELECT *
  FROM [table]
ORDER BY score""").fetchall()[::-1]
player = cur.execute(f"""SELECT score,
       nickname
  FROM [table]
 WHERE id = {n};""").fetchall()[0]
print(player)
results = list(sorted(results, key=lambda x: int(x[1]), reverse=True))
print((list(results[0])[1]))


def main_table():
    global done
    clock = pygame.time.Clock()
    done = False
    quit = Button(screen.get_size()[0] / 2 - 90, (screen.get_size()[1] / 3) * 2, 'Return', typ=5, group=btn_sprites_2)
    while not done:
        screen.fill((30, 30, 30))
        btn_sprites_1_1.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                btn_sprites_1_1.update(event)

            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
        dog = pygame.image.load('data/table.png')
        dog_rect = dog.get_rect()
        dog_rect[0] = screen.get_size()[0] / 3 - 10
        dog_rect[1] = screen.get_size()[1] / 10 * 2
        screen.blit(dog, dog_rect)
        text_img1 = font.render('Игра завершена: ', True, text_col)
        text_img2 = font.render('Таблица рекордов: ', True, text_col)
        text_img3 = font.render('Статистика: ', True, text_col)
        text_img4 = font.render('Cчёт: ', True, text_col)
        text_img5 = font.render(f'{player[0]}', True, text_col)
        text_img6 = font.render('Имя:', True, text_col)
        text_img7 = font.render(f'{player[1]}', True, text_col)
        screen.blit(text_img1, (screen.get_size()[0] / 2 - 100, screen.get_size()[1] / 10 * 2))
        screen.blit(text_img2, (screen.get_size()[0] / 3, screen.get_size()[1] / 10 * 3))
        screen.blit(text_img3, (screen.get_size()[0] / 3 * 2 - 100, screen.get_size()[1] / 10 * 3))
        screen.blit(text_img4, ((screen.get_size()[0] / 3 * 2) - 100, screen.get_size()[1] / 10 * 4))
        screen.blit(text_img5, ((screen.get_size()[0] / 3 * 2), screen.get_size()[1] / 10 * 4))
        screen.blit(text_img6, (screen.get_size()[0] / 3 * 2 - 100, screen.get_size()[1] / 10 * 5))
        screen.blit(text_img7, (screen.get_size()[0] / 3 * 2, screen.get_size()[1] / 10 * 5))
        btn_sprites_2.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                btn_sprites_2.update(event)
        btn_sprites_2.update()
        #screen.blit(text_img5, (screen.get_size()[0] / 2, 300))
        for i in range(n):
            text_img = font.render(' '.join(list(map(lambda x: str(x), list(results[i])[1:]))), True, text_col)
            text_len = text_img.get_width()
            screen.blit(text_img, (screen.get_size()[0] / 3, screen.get_size()[1] / 10 * (i + 4)))
        pygame.display.flip()

        clock.tick(30)
    pygame.quit()

main_table()
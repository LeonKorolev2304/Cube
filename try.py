import pygame
import random
import sys
import os
import threading
import math
from PIL import Image
from PIL import ImageGrab, ImageOps
import sqlite3




# Меню (Играть, таблица лидеров, выход) Если Играть то представстесь после этого закрытие файла и запуск программы по окончанию программа выводит счет и таблицу лидеров и только кнопка вернутся
clicked = False
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
btn_sprites_1_1 = pygame.sprite.Group()
font = pygame.font.SysFont('arial', 30)
font = pygame.font.SysFont('Constantia', 30)
FONT = pygame.font.Font(None, 32)
text_col = black
con = sqlite3.connect("data2.sqlite")
cur = con.cursor()

n = cur.execute(f"""SELECT MAX(id)
  FROM [table]""").fetchall()[0][0]

results = cur.execute(f"""SELECT *
  FROM [table]
ORDER BY score""").fetchall()[::-1]

print(results)
print((list(results[0])[1]))


def main():
    global done
    clock = pygame.time.Clock()
    done = False
    while not done:
        screen.fill((30, 30, 30))
        btn_sprites_1_1.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                btn_sprites_1_1.update(event)

            if event.type == pygame.QUIT:
                done = True
                pygame.quit()

        text_img = font.render('Таблица рекордов: ', True, text_col)
        text_len = text_img.get_width()
        screen.blit(text_img, (screen.get_size()[0] / 2 - 100, 100))
        for i in range(n):
            text_img = font.render(str(i + 1) + ') Очки: ' + ' '.join(list(map(lambda x: str(x), list(results[i])[1:]))), True, text_col)
            text_len = text_img.get_width()
            screen.blit(text_img, (screen.get_size()[0] / 2 - 100, 100 * (i + 2)))

        btn_sprites_1_1.update()

        pygame.display.flip()

        clock.tick(30)
    pygame.quit()

main()
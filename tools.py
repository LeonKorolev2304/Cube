import os
import sys

import pygame

FPS = 50
WIDTH = 1920
HEIGHT = 1020


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


def terminate():
    pygame.quit()
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

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
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


def end_screen(screen):
    intro_text = ["Таблица рекордов".ljust(150, ' ') + "Статистика",
                  "",
                  "1 -".ljust(150, ' ') + "Убито врагов:",
                  "2 -".ljust(150, ' ') + "Собрано опыта:",
                  "3 -".ljust(150, ' ') + "Собрано очков здоровья:",
                  "4 -".ljust(150, ' ') + "Получено усилителей:",
                  "5 -",
                  "6 -",
                  "7 -",
                  "8 -",
                  "9 -",
                  "10 -"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
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
            '''elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return 0'''
        pygame.display.flip()
        clock.tick(FPS)

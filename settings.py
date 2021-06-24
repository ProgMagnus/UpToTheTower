import pygame as pg
from os import path

img_dir = path.join(path.dirname(__file__), 'img')

TITLE = "Up to the tower!"
WIDTH = 600
HEIGHT = 600
FPS = 60
HS_FILE = 'highscore.txt'
KNIGHT = 'knight01.png'
Ground = 'spritesheet_jumper.png'
Mobster = 'Flappy Dragon Characters.png'
Goblins = 'goblins.png'

PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 40

BOOST_POWER = 60
POW_SPAWN_PCT = 15
Goblin_spawn_pct = 15
Health_spawn_pct = 7
MOB_FREQ = 5000
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2
CLOUD_LAYER = 0

PLATFORM_LIST = [(5, HEIGHT - 400),
                 (WIDTH / 2 - 90, HEIGHT * 3 / 4 - 20),
                 (100, HEIGHT - 300),
                 (350, 210),
                 (175, 75)]

SPAWN_POINT = [(5, HEIGHT - 60),
                 (WIDTH / 2 + 70, HEIGHT * 3 / 4 + 70)]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE
background = pg.image.load(path.join(img_dir, 'background.png'))
background_rect = background.get_rect()
start_screen = pg.image.load(path.join(img_dir, 'startscreen.png'))
start_screen_rect = background.get_rect()
info_screen = pg.image.load(path.join(img_dir, 'info.png'))
info_screen_rect = background.get_rect()
import time
from random import randint

import pygame as pg

pg.init()

screen = pg.display.set_mode((1792, 896), pg.RESIZABLE)

pg.display.set_caption('snake Game')
pg.display.set_icon(pg.image.load('icon.png'))
appleIMG = pg.image.load('apple.png')

running = True
game = True

class segment:
    x = 0
    y = 0
    facing = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.facing = facing

    def getGridX(self):
        return self.x * 32

    def getGridY(self):
        return self.y * 32

facing = [0, -1]
tempfacing = facing

body = [segment(12, 12), segment(12, 13), segment(12, 14), segment(12, 15), ]
size = 4
facings = [1, 1, 1, 1]

applePos = [randint(0, 22), randint(0, 22)]

def getGroundStart():
    return screen.get_width() // 2 - 384, screen.get_height() // 2 - 384

def getGroundStartX():
    return screen.get_width() // 2 - 384

def getGroundStartY():
    return screen.get_height() // 2 - 384

def gameOver():
    screen.fill((32, 149, 23))
    screen.blit(pg.image.load('gameOverpng.png'), (screen.get_width() // 2 - 640, screen.get_height() // 2 - 360))

    font = pg.font.SysFont(None, 120)
    img = font.render(f'{size}', True, (0, 0, 0))
    screen.blit(img, (screen.get_width() // 2 - 640 + 759, screen.get_height() // 2 - 360 + 169))

    font = pg.font.SysFont(None, 120)
    img = font.render(f'{moves}', True, (0, 0, 0))
    screen.blit(img, (screen.get_width() // 2 - 640 + 759, screen.get_height() // 2 - 360 + 260))

    boolean = True
    while boolean:
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                boolean = False

start_time = time.time() - 0.5
moves = 0
while running:
    current_time = time.time()
    elapsed_time = current_time - start_time

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                if not facing[0] == 0:
                    tempfacing = [0, -1]

            if event.key == pg.K_DOWN:
                if not facing[0] == 0:
                    tempfacing = [0, 1]

            if event.key == pg.K_RIGHT:
                if not facing[1] == 0:
                    tempfacing = [1, 0]

            if event.key == pg.K_LEFT:
                if not facing[1] == 0:
                    tempfacing = [-1, 0]

    if elapsed_time > 1:

        facing = tempfacing
        start_time = time.time()

        screen.fill((32, 149, 23))

        screen.fill((52, 179, 33), (getGroundStart(), (768, 768)))

        body.insert(0, segment(body[0].x + facing[0], body[0].y + facing[1]))
        facings.insert(0, facing)

        if body[0].x < 0 or body[0].x > 23 or body[0].y < 0 or body[0].y > 23:
            running = False
            gameOver()

        match = 0
        for seg in body:
            if body[0].x == seg.x and body[0].y == seg.y:
                match += 1
            if match > 1:
                running = False
                gameOver()

        if [body[0].x, body[0].y] == applePos:
            size += 1
            if size > 575:
                running = False
                gameOver()

            nope = 0
            while nope == 0:
                nope = 1
                applePos = [randint(0, 22), randint(0, 22)]

                for seg in body:
                    if [seg.x, seg.y] == applePos:
                        nope = 0

        while len(facings) > size:
            facings.pop()
            body.pop()

        for i in range(0, 800, 32):
            swith = screen.get_width() // 2 - 384
            sheight = screen.get_height() // 2 - 384
            screen.fill((0, 0, 0), ((swith + i, sheight), (1, 768)))

        for i in range(0, 800, 32):
            swith = screen.get_width() // 2 - 384
            sheight = screen.get_height() // 2 - 384
            screen.fill((0, 0, 0), ((swith, sheight + i), (768, 1)))

        screen.blit(appleIMG,
                    ((getGroundStartX() + applePos[0] * 32 + 1, getGroundStartY() + applePos[1] * 32 + 1), (getGroundStartX() + applePos[0] * 32 + 31, getGroundStartY() + applePos[1] * 32 + 31)))

        surface = pg.Surface((768, 768), pg.SRCALPHA)
        for i in range(1, size):
            # screen.fill((255, 0, 0), ((getGroundStartX() + seg.getGridX() + 1, getGroundStartY() + seg.getGridY() + 1), (31, 31)))
            pg.draw.line(surface, (255, 0, 0), [body[i].getGridX() + 15, body[i].getGridY() + 15], [body[i - 1].getGridX() + 15, body[i - 1].getGridY() + 15], 20)
        screen.blit(surface, ((getGroundStartX(), getGroundStartY()), (getGroundStartX() + 768, getGroundStartY() + 768)))

        font = pg.font.SysFont(None, 24)
        img = font.render(f'score: {size}   time: {moves},', True, (0, 0, 0))
        screen.blit(img, (getGroundStartX(), getGroundStartY() - 20))

        moves += 1
        pg.display.update()

import pygame
from pygame.locals import *
import os
import sys
import math
import random

pygame.init()

W, H = 800, 447
win = pygame.display.set_mode((W,H))
pygame.display.set_caption('Side Scroller')

bg = pygame.image.load(os.path.join('images','bg.png'))
bgX = 0
bgX2 = bg.get_width()

clock = pygame.time.Clock()

class Player(object):
    run = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(8,16)]
    jump = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(1,8)]
    fall = pygame.image.load(os.path.join('images', '0.png'))
    slide = [pygame.image.load(os.path.join('images', 'S1.png')),pygame.image.load(os.path.join('images', 'S2.png')),pygame.image.load(os.path.join('images', 'S2.png')),pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')),pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S3.png')), pygame.image.load(os.path.join('images', 'S4.png')), pygame.image.load(os.path.join('images', 'S5.png'))]
    jumpList = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.jumpCount = 0
        self.sliding = False
        self.slideCount = 0
        self.runCount = 0
        self.falling = False

    def draw(self, win):
        if self.falling:
            win.blit(self.fall, (self.x, self.y + 30))
        elif self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 1.2
            win.blit(self.jump[self.jumpCount//18], (self.x,self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0

            self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 10)
        elif self.sliding:
            if self.slideCount < 20:
                self.y += 1
            elif self.slideCount == 80:
                self.y -= 19
            elif self.slideCount > 20 and self.slideCount < 80:
                self.hitbox = (self.x, self.y + 3, self.width - 8, self.height - 35)

            if self.slideCount >= 110:
                self.sliding = False
                self.slideCount = 0
                self.runCount = 0
                self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 10)
            win.blit(self.slide[self.slideCount//10], (self.x,self.y))
            self.slideCount += 1
            
        else:
            if self.runCount > 42:
                self.runCount = 0
            win.blit(self.run[self.runCount//6], (self.x,self.y))
            self.runCount += 1
            self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 13)
        # pygame.draw.rect(win, (155,0,0), self.hitbox, 2) # HITBOX

class Saw(object):
    img = [pygame.image.load(os.path.join('images', 'SAW0.png')),pygame.image.load(os.path.join('images', 'SAW1.png')),pygame.image.load(os.path.join('images', 'SAW2.png')),pygame.image.load(os.path.join('images', 'SAW3.png'))]
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (x,y,width,height)
        self.count = 0

    def draw(self, win):
        self.hitbox = (self.x + 5, self.y + 7, self.width - 16, self.height - 15)
        if self.count >= 8:
            self.count = 0
        win.blit(pygame.transform.scale(self.img[self.count//2], (60, 60)), (self.x, self.y))
        self.count += 1
        # pygame.draw.rect(win, (255,0,0), self.hitbox, 2) # HITBOX

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False


class Spike(Saw):
    img = pygame.image.load(os.path.join('images', 'spike.png'))
    def draw(self, win):
        self.hitbox = (self.x + 15, self.y, 17, 315)
        win.blit(self.img, (self.x, self.y))
        # pygame.draw.rect(win, (255,0,0), self.hitbox, 2) # HITBOX

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] < self.hitbox[3]:
                return True
        return False

def redrawWindow():
    win.blit(bg, (bgX, 0))
    win.blit(bg, (bgX2, 0))
    runner.draw(win)
    for objectt in objects:
        objectt.draw(win)
    font = pygame.font.Font('font.ttf', 30)
    text = font.render('Score: ' + str(score), 1, (150,150,150))
    win.blit(text, (W - text.get_width() - 10, 10))
    pygame.display.update()

def updateFile():
    f = open('score.txt', 'r')

    file = f.readlines()
    try:
        last = int(file[0])

        if last < int(score):
            f.close()
            file = open('score.txt', 'w')
            file.write(str(score))
            file.close()

            return score
        return last
    except:
        return '0'

def endScreen():
    global pause, objects, speed, score
    pause = 0
    objects = []
    speed = 30

    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                run = False

        win.blit(bg, (0,0))
        largeFont = pygame.font.Font('font.ttf', 80)
        smallFont = pygame.font.Font('font.ttf', 60)
        prevoiusScore = largeFont.render('Prevoius Score: ' + str(updateFile()), 1, (200,255,255))
        win.blit(prevoiusScore, (W/2 - prevoiusScore.get_width()/2, H/2 - prevoiusScore.get_height()/2))

        newScore = largeFont.render('Score: ' + str(score), 1, (200,255,255))
        win.blit(newScore, (W/2 - newScore.get_width()/2, H/2 - newScore.get_height()/2 + 70))
        TapText = smallFont.render('TAP TO PLAY AGAIN', 1, (10,10,10))
        win.blit(TapText, (W/2 - TapText.get_width()/2, H - TapText.get_height() - 10))
        pygame.display.update()

    score = 0
    runner.falling = False
    runner.jumping = False
    runner.jumpCount = 0
    runner.y = 313
    runner.sliding = False

# Game loop
runner = Player(220, 313, 64, 64)
pygame.time.set_timer(USEREVENT+1, 500)
pygame.time.set_timer(USEREVENT+2, random.randrange(3000,5000))
speed = 30

pause = 0
fallSpeed = 0
objects = []

while True:
    score = speed//5 - 6
    keys = pygame.key.get_pressed()
    if pause > 0:
        pause += 1
        if pause > fallSpeed *2:
            endScreen()

    for objectt in objects:
        if objectt.collide(runner.hitbox):
            runner.falling = True

            if pause == 0:
                fallSpeed = speed
                pause  = 1

        objectt.x -= 1.4
        if objectt.x < objectt.width * -1:
            objects.pop(objects.index(objectt))

    bgX -=1.4
    bgX2 -= 1.4
    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()
    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            quit()

        if event.type == USEREVENT+1:
            speed += 1

        if event.type == USEREVENT+2:
            r = random.randrange(0,2)
            if r == 0:
                objects.append(Saw(810,310,64,64))
            else:
                objects.append(Spike(810,0,48,320))

    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
        if not(runner.jumping):
            runner.jumping = True

    if keys[pygame.K_DOWN]:
        if not(runner.sliding):
            runner.sliding = True

    clock.tick(speed)
    redrawWindow()
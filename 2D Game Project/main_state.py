import random
import json
import os

from pico2d import *

import game_framework
import title_state

name = "MainState"

boy = None
grass = None
background = None
moon = None
font = None
stars = None

class Shooting_Star:
    def __init__(self):
        self.image = load_image('Star.png')
        self.x = random.randint(-100, 700)
        self.y = 600
        self.isstate = 1
        self.speed = random.randint(5,10)
        self.size = random.randint(1,2)
    def update(self):
        self.x += self.speed
        self.y -= self.speed
        #delay(0.05)
        if (self.x >= 800 or self.y <= 0):
            self.isstate = 0
            #del(self)
    def draw(self):
        #self.image.draw(self.x, self.y)
        self.image.clip_draw(0, 0, 34, 34, self.x, self.y, 15 * self.size, 15 * self.size)

class Moon:
    def __init__(self):
        self.image = load_image('platformertiles.png')
        self.x = 670
        self.y = 500
        self.speed = 1
    def update(self):
        if boy.ismove == 1:
            self.x += self.speed
    def draw(self):
        self.image.clip_draw(32 * 3, 32 * 2, 32, 32, self.x, self.y, 80, 80)

class Star:
    def __init__(self):
        self.image = load_image('platformertiles.png')
        self.x = 20
        self.y = 20
        self.frame = random.randint(0,2)
        self.time = 5.0
        self.speed = 1
        self.state = 0
    def update(self):
        if self.time >= 5.0:
            self.state = random.randint(0, 20)
            self.time = 0
        if boy.ismove == True:
            self.x += self.speed
        self.time += 0.1
    def draw(self, i, j):
        self.image.clip_draw((32 * (5 + self.frame)), 32, 32, 32, i * 40, j * 40, 80, 80)

class BackGround:
    def __init__(self):
        self.Backimage = load_image('platformertiles.png')
        self.star_time = 5.0
        self.star = [[0]*15 for i in range(20)]
        self.star_frame = [[0]*15 for i in range(20)]
        self.speed = 0

    def update(self):
        if self.star_time >= 5:
            for i in range(20):
                for j in range(15):
                    self.star[i][j] = random.randint(1, 20)
                    self.star_frame[i][j] = random.randint(0,2)
                    self.star_time = 0
        if boy.ismove == True and boy.state == 1:
            self.speed = -1
        elif boy.ismove == True and boy.state == 2:
            self.speed = 1
        else:
            self.speed = 0
        self.star_time += 0.1

    def draw(self):
        self.Backimage.clip_draw(32 * 3, 32, 32, 32, 0, 0, 1600, 1200)                      #Back
        for i in range(20):
            for j in range(15):
                if self.star[i][j] == 1:
                    self.Backimage.clip_draw((32 * (5 + self.star_frame[i][j])), 32, 32, 32, i * 40 + self.speed, j * 40 + self.speed, 80, 80)  #star

class Grass:
    def __init__(self):
        self.image = load_image('platformertiles.png')
        self.frame = 0

    def update(self):
        self.frame = (self.frame + 1) % 8

    def draw(self):
        #self.image.draw(400, 30)
        for i in range(16):
            self.image.clip_draw(32, 32*2, 32, 32, i * 50, 0,100,100)

class Boy:
    RIGHT_RUN = 1
    LEFT_RUN = 2
    RIGHT_STAND = 3
    LEFT_STAND = 4
    JUMP = 5

    def __init__(self):
        self.RIGHT_RUN_image = load_image('CH_RIGHT_RUN.png')
        self.LEFT_RUN_image = load_image('CH_LEFT_RUN.png')
        self.RIGHT_STAND_image = load_image('CH_RIGHT_STAND.png')
        self.LEFT_STAND_image = load_image('CH_LEFT_STAND.png')
        self.x, self.y = 0, 100
        self.frame = 0
        self.state = self.RIGHT_STAND
        self.speed = 10
        self.ismove = False
        self.isjump = False
        self.isreach = False

    def update(self):
        self.frame = (self.frame + 1) % 3
        self.handle_state[self.state](self)
        if self.x <= 0:
            self.x = 1
        if self.ismove == True:
            self.x += self.speed
        if (self.y <= 180 and self.isjump == True and self.isreach == False):
            self.y += 20
        if self.y >= 180:
            self.isreach = True
        if self.isreach == True:
            self.y -= 20
        if self.y <= 100:
            self.isreach = False
            self.isjump = False

    def draw(self):
        self.image.clip_draw(self.frame * 34, 0, 33, 39, self.x, self.y, 80, 100)

    def handle_right_run(self):
        self.image = self.RIGHT_RUN_image

    def handle_left_run(self):
        self.image = self.LEFT_RUN_image

    def handle_right_stand(self):
        self.image = self.RIGHT_STAND_image

    def handle_left_stand(self):
        self.image = self.LEFT_STAND_image

    def handle_jump(self):
        pass

    handle_state = {
        RIGHT_RUN: handle_right_run,
        LEFT_RUN: handle_left_run,
        RIGHT_STAND: handle_right_stand,
        LEFT_STAND: handle_left_stand,
        JUMP: handle_jump
    }

def enter():
    global boy, grass
    global background
    global moon
    global stars
    background = BackGround()
    boy = Boy()
    grass = Grass()
    moon = Moon()
    stars = [Shooting_Star() for i in range(10)]
    #open_canvas()

def exit():
    global boy, grass
    global background
    global moon
    global stars
    del(background)
    del(boy)
    del(grass)
    del(moon)
    del(stars)

def pause():
    pass

def resume():
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.change_state(title_state)
            elif event.key == SDLK_LEFT:
                boy.state = boy.LEFT_RUN
                #boy.x -= boy.speed
                boy.ismove = True
                boy.speed = -10
                if (moon.x <= 670):
                    moon.speed = 3
            elif event.key == SDLK_RIGHT:
                boy.state = boy.RIGHT_RUN
                #boy.x += boy.speed
                boy.ismove = True
                boy.speed = 10
                if (moon.x >= 130):
                    moon.speed = -3
            elif event.key == SDLK_UP:
                if boy.isjump == False:
                    boy.isjump = True

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT:
                boy.state = boy.LEFT_STAND
                boy.ismove = False
            elif event.key == SDLK_RIGHT:
                boy.state = boy.RIGHT_STAND
                boy.ismove = False

current_time = get_time()

def update():
    global current_time
    global stars
    global back_stars
    background.update()
    for i in range(10):
        stars[i].update()
        if stars[i].isstate == 0:
            stars[i] = Shooting_Star()
    #for star in stars:
    boy.update()
    grass.update()
    moon.update()

    delay(0.05)

    frame_time = get_time() - current_time
    frame_rate = 1.0 / frame_time
    print("Frame Rate : %f fps, Frame Time : %f sec," % (frame_rate, frame_time))

    current_time += frame_time


def draw():
    global stars
    clear_canvas()
    background.draw()
    for i in range(10):
        stars[i].draw()
    moon.draw()
    grass.draw()
    boy.draw()
    update_canvas()







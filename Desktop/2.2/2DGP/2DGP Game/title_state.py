import game_framework
import os
from pico2d import *

import main_state

name = "TitleState"
image = None


def enter():
    global image
    image = load_image('Main.png')
    pass

def exit():
    global image
    del(image)
    #close_canvas()
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(main_state)

    pass

def draw():
    clear_canvas()
    image.clip_draw(0, 0, 1500, 850, 0, 0, 1600, 1200)
    update_canvas()
    pass







def update():
    pass


def pause():
    pass


def resume():
    pass







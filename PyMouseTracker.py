import os
import sys
import time
import functools
import turtle

import screeninfo
import yaml

from pynput import keyboard, mouse

def on_move(x: int, y: int):
    global pos_list
    global mw, mh
    pos_list.append((x - mw / 2, mh / 2 - y))

def turtle_draw() -> None:
    global pos_list

    turtle.penup()
    turtle.goto(pos_list[0])
    turtle.pendown()

    for x, y in pos_list[1:]:
        turtle.seth(turtle.towards(x, y))
        turtle.goto(x, y)

def turtle_init() -> None:
    global mw, mh
    turtle.hideturtle()
    turtle.Screen().setup(mw + 4, mh + 8)
    turtle.color('red')
    turtle.speed('fastest')


def save(file_name: str) -> None:
    turtle.getscreen().getcanvas().postscript(file=f'temp/{file_name}.ps')
    turtle.bye()


def stop_mouse_listener(*args) -> None:
    global mouse_listener
    mouse_listener.stop()


def stop_keyboard_listener() -> None:
    global keyboard_listener

    keyboard_listener.stop()
    stop_mouse_listener()


def for_canonical(f):
    return lambda k: f(keyboard_listener.canonical(k))


pos_list = []

monitors = screeninfo.get_monitors(Enumerator.OSX if sys.platform == 'darwin' else None)
mw, mh = monitors[0].width, monitors[0].height


if __name__ == '__main__':
    os.makedirs('temp', exist_ok=True)
    os.makedirs('out', exist_ok=True)
    
    if not os.path.exists('config.yml'):
        print('No config file found!')
        print('Creating one...')

        with open('config.yml', 'w', encoding='utf-8') as config_file:
            yaml.dump({ 'ghostscript_path': None }, config_file)
            sys.exit()
    else:
        with open('config.yml', 'r', encoding='utf-8') as conf_file:
            config = yaml.load(conf_file, Loader=yaml.CLoader)
            
        if not config["ghostscript_path"]:
            print('Please set GhostScript path in the config.yml file!')
            sys.exit()
            
    file_name = f'{int(time.time())}-{mw}x{mh}'
    turtle_init()
 
    print('To stop recording, press "<ctrl>+<alt>+h"')
    
    mouse_listener = mouse.Listener(on_move=on_move)
    mouse_listener.start()

    hotkey = keyboard.HotKey(
        keyboard.HotKey.parse('<ctrl>+<alt>+h'),
        stop_keyboard_listener
    )
    
    with keyboard.Listener(
        on_press=for_canonical(hotkey.press)
    ) as keyboard_listener:
        keyboard_listener.join()

    print('To start drawing, click any mouse button')
    
    with mouse.Listener(on_click=stop_mouse_listener) as mouse_listener:
        mouse_listener.join()

    turtle_draw()
    save(file_name)

    os.system(
        f'""{config["ghostscript_path"]}" -sDEVICE=png16m -g{mw}x{mh} -o "out/{file_name}.png" "temp/{file_name}.ps"'
    )

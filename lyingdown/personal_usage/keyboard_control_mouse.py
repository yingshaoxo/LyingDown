from pynput.keyboard import Key, Listener
from pynput.mouse import Button, Controller

mouse = Controller()

state = {
            'ctrl': False,
            'speed': 1,
        }

def on_press(key):
    #print('pressed:', key)
    if key == Key.ctrl:
        state['ctrl'] = True
    if state['ctrl'] == True:
        state['speed'] += 1
        speed = state['speed']
        if key == Key.left:
            mouse.move(-speed, 0)
        elif key == Key.right:
            mouse.move(speed, 0)
        elif key == Key.up:
            mouse.move(0, -speed)
        elif key == Key.down:
            mouse.move(0, speed)

def on_release(key):
    #print('released:', key)
    if key == Key.ctrl:
        state['ctrl'] = False
        state['speed'] = 5

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

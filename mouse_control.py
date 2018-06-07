from pynput.keyboard import Listener as KeyboardListener
#from pynput.keyboard import Controller as KeyboardController
#from pynput.keyboard import Key
from pynput.mouse import Controller as MouseController
from pynput.mouse import Button


DISTANCE = 15

mouseControl = MouseController()

ctrl_status = 0


def on_press(key):
    try:
        k = key.char
    except:
        k = key.name
    print(k)

    global ctrl_status
    if k == "ctrl":
        ctrl_status = 1

    if ctrl_status == 1:
        handle_press(k)


def on_release(key):
    try:
        k = key.char
    except:
        k = key.name
    print(k)

    global ctrl_status
    if k == "ctrl":
        ctrl_status = 0

    handle_release(k)


def handle_press(k):
    if k == "up":
        mouseControl.move(0, -DISTANCE)
    elif k == "down":
        mouseControl.move(0, DISTANCE)
    elif k == "left":
        mouseControl.move(-DISTANCE, 0)
    elif k == "right":
        mouseControl.move(DISTANCE, 0)
    elif k == "enter":
        mouseControl.click(Button.left)

    elif k == "0":
        mouseControl.press(Button.left)


def handle_release(k):
    if k == "0":
        mouseControl.release(Button.left)


keyListen = KeyboardListener(on_press=on_press, on_release=on_release)
keyListen.start()
keyListen.join()

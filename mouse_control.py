from pynput.keyboard import Listener as KeyboardListener
#from pynput.keyboard import Controller as KeyboardController
#from pynput.keyboard import Key
from pynput.mouse import Controller as MouseController
from pynput.mouse import Button


DISTANCE = 20

mouseControl = MouseController()


def on_press(key):
    try:
        k = key.char
    except:
        k = key.name
    print(k)
    if k == "up":
        mouseControl.move(0, -DISTANCE)
    elif k == "down":
        mouseControl.move(0, DISTANCE)
    elif k == "left":
        mouseControl.move(-DISTANCE, 0)
    elif k == "right":
        mouseControl.move(DISTANCE, 0)
    elif k == "num_lock":
        mouseControl.click(Button.left)


keyListen = KeyboardListener(on_press=on_press)
keyListen.start()
keyListen.join()

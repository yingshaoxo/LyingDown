import numpy as np
import pyscreenshot as ImageGrab
import pyautogui
import cv2


class VideoCamera(object):
    def __init__(self, num):
        self.num = num

        self.screen_width = pyautogui.size()[0]
        self.screen_height = pyautogui.size()[1]

        if num == 1:
            self.top_left = (self.screen_width//2, 0)
            self.lower_right = (self.screen_width, self.screen_height//2)
        elif num == 2:
            self.top_left = (self.screen_width//2, self.screen_height//2)
            self.lower_right = (self.screen_width, self.screen_height)

        self.cursor = cv2.resize(cv2.imread('cursor.png'), (10, 10))
        # self.top_left = (0, 0)
        # self.lower_right = (self.screen_width, self.screen_height)

    def get_frame(self):
        frame = np.array(ImageGrab.grab(bbox=(
            self.top_left[0], self.top_left[1], self.lower_right[0], self.lower_right[1])))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = self.add_cursor(frame)

        ret, png = cv2.imencode('.png', frame)
        return png.tobytes()

    def get_test_frame(self):
        frame = np.array(ImageGrab.grab(bbox=(
            self.top_left[0], self.top_left[1], self.lower_right[0], self.lower_right[1])))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = self.add_cursor(frame)
        return frame

    def add_cursor(self, frame):
        x, y = pyautogui.position()
        xx, yy = x+self.cursor.shape[0], y+self.cursor.shape[1]
        if x >= self.top_left[0] and y >= self.top_left[1] and xx <= self.lower_right[0] and yy <= self.lower_right[1]:
            x, y = x-self.top_left[0], y-self.top_left[1]
            xx, yy = x+self.cursor.shape[0], y+self.cursor.shape[1]
            frame[y:yy, x:xx] = self.cursor
        return frame


if __name__ == "__main__":
    vc = VideoCamera(1)
    while 1:
        frame = vc.get_test_frame()
        cv2.imshow('hi', frame)
        if cv2.waitKey(1) == 27:
            break  # esc to quit

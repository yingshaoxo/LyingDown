import numpy as np
import pyscreenshot as ImageGrab
import pyautogui
import cv2


class VideoCamera(object):
    def __init__(self, num):
        self.screen_width = pyautogui.size()[0]
        self.screen_height = pyautogui.size()[1]

        self.cursor = cv2.resize(cv2.imread('lyingdown/cursor.png'), (15, 15))

    def get_frame(self):
        frame = np.array(ImageGrab.grab())
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame = self.add_cursor(frame)
        # frame = self.sharp(frame)

        return frame

    def get_png(self):
        frame = self.get_frame()
        ret, png = cv2.imencode('.png', frame)
        return png.tobytes()

    def get_jpg(self):
        frame = self.get_frame()
        ret, jpg = cv2.imencode('.jpg', frame)
        return jpg.tobytes()

    def add_cursor(self, frame):
        try:
            x, y = pyautogui.position()
        except Exception as e:
            print(e)
            return frame
        xx, yy = x+self.cursor.shape[0], y+self.cursor.shape[1]
        if x >= 0 and y >= 0 and xx <= self.screen_width and yy <= self.screen_height:
            frame[y:yy, x:xx] = self.cursor
        return frame

    def sharp(self, frame):
        # Create our shapening kernel, it must equal to one eventually
        kernel_sharpening = np.array([[-1, -1, -1],
                                      [-1, 9, -1],
                                      [-1, -1, -1]])

        # applying the sharpening kernel to the input image & displaying it.
        sharpened = cv2.filter2D(frame, -1, kernel_sharpening)
        return sharpened


if __name__ == "__main__":
    vc = VideoCamera(0)
    while 1:
        frame = vc.get_frame()
        cv2.imshow('hi', frame)
        if cv2.waitKey(1) == 27:
            break  # esc to quit

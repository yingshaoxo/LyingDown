import numpy as np
#import pyscreenshot as ImageGrab
from PIL import ImageGrab
from mss import mss, tools
import pyautogui
import cv2
from sys import platform


class VideoCamera(object):
    def __init__(self, num):
        self.is_linux = True
        if platform == "linux" or platform == "linux2":
            self.is_linux = True
        else:
            self.is_linux = False

        self.screen_width = pyautogui.size()[0]
        self.screen_height = pyautogui.size()[1]

        cursor_img = np.ones((18, 18, 3), dtype = np.uint8)
        cursor_img = 255 * cursor_img
        for num1 in [7, 8, 9, 10, 11]:
            for num2 in [7, 8, 9, 10, 11]:
                cursor_img[num1][num2][0] = 0
                cursor_img[num1][num2][1] = 0
                cursor_img[num1][num2][2] = 0

        # dir_path = os.path.dirname(os.path.realpath(__file__))
        # cursor_path = os.path.join(dir_path, "cursor.png")
        # self.cursor = cv2.resize(cv2.imread(cursor_path), (15, 15))

        self.cursor = cv2.resize(cursor_img, (15, 15))
        self.mss = mss(with_cursor=True, compression_level=1)
    
    def get_png_by_another_method(self):
        img_ = self.mss.grab(self.mss.monitors[0])
        return tools.to_png(img_.rgb, img_.size)

    def get_frame(self):
        if self.is_linux:
            frame = np.array(ImageGrab.grab(xdisplay="")) # type: ignore
        else:
            frame = np.array(ImageGrab.grab(include_layered_windows=True))

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame = self.add_cursor(frame)

        return frame
    
    def get_png(self):
        frame = self.get_frame()
        ret, png = cv2.imencode('.png', frame)
        return png.tobytes()

    def get_jpg(self):
        frame = self.get_frame()
        #frame = cv2.resize(frame, dsize=(1920, 1080), interpolation=cv2.INTER_LINEAR)
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

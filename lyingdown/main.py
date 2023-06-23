from typing import Callable
from flask import Flask, render_template, Response, request, make_response
from lyingdown.screen_camera import VideoCamera, pyautogui


app = Flask(__name__)
pyautogui.FAILSAFE = False
the_camera = VideoCamera(0)


@app.route('/')
def index():
    return render_template('index.html')


def a_screenshot_generator(a_camera: VideoCamera):
    while True:
        frame = a_camera.get_png()
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video<int:num>')
def video(num):
    return Response(a_screenshot_generator(VideoCamera(num)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/image/<int:random_number>')
def image(random_number=0):
    image_binary = the_camera.get_png()
    response = make_response(image_binary)
    response.headers.set('Content-Type', 'image/png')
    response.headers.set(
        'Content-Disposition', 'attachment', filename='%s.png' % random_number)
    return response

done_dict = {}
def my_debounce(id: str, func: Callable):
    global done_dict
    done = done_dict.get(id)

    if done is not False: # None or True
        done_dict[id] = False
        func()
        done_dict[id] = True


@app.route('/mouse_move', methods = ['POST'])
def mouse_move():
    global the_camera

    data_object = request.json
    if (data_object != None):
        percent_x = data_object.get('percent_x')
        percent_y = data_object.get('percent_y')
        x = int(percent_x * the_camera.screen_width)
        y = int(percent_y * the_camera.screen_height)

        my_debounce("mouse_move", lambda : pyautogui.moveTo(x,y))

    return ""


@app.route('/mouse_left_click', methods = ['POST'])
def mouse_left_click():
    data_object = request.json

    if (data_object != None):
        percent_x = data_object.get('percent_x')
        percent_y = data_object.get('percent_y')
        x = int(percent_x * the_camera.screen_width)
        y = int(percent_y * the_camera.screen_height)

        my_debounce("mouse_left_click", lambda : pyautogui.leftClick(x, y))

    return ""


def main():
    if "__compiled__" in globals():
        app.run(host='0.0.0.0')
    else:
        app.run(host='0.0.0.0', debug=True)


if __name__ == '__main__':
    main()

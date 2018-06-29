from flask import Flask, render_template, Response
from screen_camera import VideoCamera

# from auto_everything.base import Terminal
# t = Terminal()
# t.run_py("mouse_control.py")


app = Flask(__name__)
cameras = [VideoCamera(0), VideoCamera(1)]


@app.route('/')
def index():
    return render_template('index.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video<int:num>')
def video_feed(num):
    global cameras
    return Response(gen(cameras[num]),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

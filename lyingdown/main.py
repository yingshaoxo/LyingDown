from flask import Flask, render_template, Response
from lyingdown.screen_camera import VideoCamera


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def gen(camera):
    while True:
        frame = camera.get_jpg()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video<int:num>')
def video_feed(num):
    global cameras
    return Response(gen(VideoCamera(num)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def main():
    if "__compiled__" in globals():
        app.run(host='0.0.0.0')
    else:
        app.run(host='0.0.0.0', debug=True)


if __name__ == '__main__':
    main()

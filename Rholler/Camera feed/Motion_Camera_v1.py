# ABANDONED ===============

from flask import Flask, Response
from picamera import PiCamera
import io

app = Flask(__name__)
camera = PiCamera(framerate=24)  # Initialize the camera here


def generate(camera):
    while True:
        stream = io.BytesIO()
        camera.capture(stream, 'jpeg', use_video_port=True)
        stream.seek(0)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + stream.read() + b'\r\n')
        stream.seek(0)
        stream.truncate()


@app.route('/video_feed')
def video_feed():
    return Response(generate(camera),  # Use the initialized camera
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    try:
        # Start the Flask application
        app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
    finally:
        camera.close()  # Properly close the camera when the script ends

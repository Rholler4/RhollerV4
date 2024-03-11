from flask import Flask, Response
import subprocess

app = Flask(__name__)

def generate_video_stream():
    # Command to capture video using libcamera-vid tool
    # The video is output to stdout (-o -), raw h264 format is used (-t 0 runs indefinitely)
    command = "libcamera-vid -o - -t 0 --inline -n --codec h264".split()

    # Open the libcamera-vid process
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1)

    while True:
        # Read video frame from stdout
        data = process.stdout.read(1024)
        if not data:
            break
        # Frame data needs to be wrapped for streaming
        yield (b'--frame\r\n'
               b'Content-Type: video/h264\r\n\r\n' + data + b'\r\n')

    # When finished, terminate the process
    process.terminate()

@app.route('/video_feed')
def video_feed():
    # Route to stream video; mimetype may need adjustment based on your video format
    return Response(generate_video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

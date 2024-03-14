# ABANDONED ===============

from flask import Flask, Response
import subprocess

app = Flask(__name__)

def generate_video_stream():
    # Command to capture video using rpicam-vid tool
    # The video is output to stdout (-o -), format is assumed to be H.264
    command = "rpicam-vid -t 0 -o -".split()

    # Open the rpicam-vid process
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=10**5)  # Increased buffer size

    while True:
        # Read video frame from stdout
        data = process.stdout.read(4096)  # Increased read size for better H.264 alignment
        if not data:
            break
        # Frame data needs to be wrapped for streaming
        yield (b'--frame\r\n'
               b'Content-Type: video/h264\r\n\r\n' + data + b'\r\n')  # Corrected MIME type for H.264

    # When finished, terminate the process
    process.terminate()

@app.route('/video_feed')
def video_feed():
    # Route to stream video; corrected mimetype for H.264
    return Response(generate_video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)

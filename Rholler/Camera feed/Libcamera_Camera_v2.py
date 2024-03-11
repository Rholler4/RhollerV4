from flask import Flask, Response
import subprocess

app = Flask(__name__)

def generate_video_stream():
    # Command to capture video using libcamera-vid tool
    # The video is output to stdout (-o -), format is set to MJPEG (-t 0 runs indefinitely)
    command = "libcamera-vid -o - -t 0 -n --codec mjpeg".split()

    # Open the libcamera-vid process
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=10**5)  # Increased buffer size

    while True:
        # Read video frame from stdout
        data = process.stdout.read(4096)  # Increased read size for better MJPEG alignment
        if not data:
            break
        # Frame data needs to be wrapped for streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n')  # Corrected for MJPEG

    # When finished, terminate the process
    process.terminate()

@app.route('/video_feed')
def video_feed():
    # Route to stream video; corrected mimetype for MJPEG
    return Response(generate_video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)

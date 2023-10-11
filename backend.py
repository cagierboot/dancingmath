from flask import Flask, send_file, jsonify

app = Flask(__name__)  # Make sure this line is before any @app.route decorators

@app.route('/')
def hello_world():
    return "Hello, World"

@app.route('/video')
def video():
    print("Video endpoint hit")
    try:
        return send_file('HomescreenVideo.mp4', mimetype='video/mp4')
    except Exception as e:
        print("Error sending file: ", e)

if __name__ == '__main__':
    app.run(debug=True)

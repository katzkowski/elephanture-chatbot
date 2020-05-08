from flask import Flask, render_template, request
from flask_socketio import SocketIO, send

app = Flask(__name__, static_url_path='/static')

app.config["SECRET_KEY"] = "Elefantengeheimnis"

socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

users = []

@app.route('/')
def send_index_page():
    return render_template('index.html')

@socketio.on('json')
def handleJson(payload):
    print("sending: " + payload)
    send(payload,json=True)


# this can be removed since it has been replaced by JSON
@socketio.on('message')
def handleMessage(msg): 
    print(request.sid)
    print('Message: ' + msg)
    send(msg, broadcast=True)

@socketio.on('username', namespace='/private')
def receive_username(username):
    users.append({username : request.sid})
    print(users)

@socketio.on('connect')
def connect():
    print("You are now connected with the server")

@socketio.on('disconnect')
def disconnect():
    print("You are disconneced from the server")

@socketio.on_error()
def error_handler(e):
    raise Exception("Some error happened, no further notice")

if __name__ == "__main__" :
    print("Try to start server...")
    socketio.run(app, host='0.0.0.0',debug = True)


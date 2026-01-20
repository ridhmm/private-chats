from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# Mengizinkan koneksi dari mana saja
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def on_join(data):
    room = data['room']
    username = data['username']
    join_room(room)
    # Notifikasi sistem bahwa user bergabung
    emit('status', {'msg': f'{username} has entered the room.'}, to=room)

@socketio.on('message')
def handle_message(data):
    room = data['room']
    # Kirim balik ke semua orang di room tersebut
    emit('new_message', {
        'msg': data['message'], 
        'user': data['username']
    }, to=room)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5002)
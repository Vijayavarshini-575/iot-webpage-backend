from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
import random
import time
from threading import Thread, Event

# Initialize Flask and Flask-SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Example patient data
patient_info = {
    "name": "Harini",
    "id": "202409301125",
    "date": "03-10-2024",
    "doctor": "Dr.M.Kannan",
    "session": "3",
    "leg": "Right"
}

# Function to generate random graph data for demonstration purposes
def generate_graph_data():
    # Graph data structure
    return {
        "graph1": [{"time": i, "x": random.uniform(-5, 5)} for i in range(20)],
        "graph2": [{"time": i, "y": random.uniform(-5, 5)} for i in range(20)],
        "graph3": [{"time": i, "z": random.uniform(-5, 5)} for i in range(20)]
    }

# Background thread to send updates periodically
def data_emitter():
    while not stop_event.is_set():
        # Send patient data
        socketio.emit('patient_data', patient_info)

        # Send graph data
        graph_data = generate_graph_data()
        socketio.emit('graph_data', graph_data)

        # Send data every 5 seconds
        socketio.sleep(5)

# Start the background thread for emitting data
stop_event = Event()
thread = Thread(target=data_emitter)
thread.start()

@app.route('/')
def index():
    return "Socket.IO server running."

# Ensure proper cleanup on exit
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')

@app.before_request
def setup():
    global stop_event, thread
    if not thread.is_alive():
        stop_event.clear()
        thread = Thread(target=data_emitter)
        thread.start()


if __name__ == '__main__':
    try:
        socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
    except KeyboardInterrupt:
        stop_event.set()
        thread.join()

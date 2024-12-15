import threading
import time
from typing import Dict, List, Optional
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

class MessageQueue:
    def __init__(self):
        self._queues: Dict[str, List[dict]] = {}
        self._locks: Dict[str, threading.Lock] = {}

    def enqueue(self, queue_name: str, message: dict) -> None:
        if queue_name not in self._locks:
            self._locks[queue_name] = threading.Lock()
            self._queues[queue_name] = []

        with self._locks[queue_name]:
            self._queues[queue_name].append(message)

    def dequeue(self, queue_name: str, timeout: float = 10.0) -> Optional[dict]:
        if queue_name not in self._locks:
            return None

        start_time = time.time()
        while time.time() - start_time < timeout / 1000.0:
            with self._locks[queue_name]:
                if self._queues[queue_name]:
                    return self._queues[queue_name].pop(0)
            time.sleep(0.1)

        return None

    def get_queue_stats(self) -> Dict[str, int]:
        return {name: len(queue) for name, queue in self._queues.items()}

app = Flask(__name__)
CORS(app)
message_queue = MessageQueue()

@app.route('/')
def index():
    queue_stats = message_queue.get_queue_stats()
    return render_template('index.html', queues=queue_stats)

@app.route('/api/<queue_name>', methods=['POST'])
def post_message(queue_name):
    message = request.get_json()
    message_queue.enqueue(queue_name, message)
    return jsonify({"status": "Message enqueued"}), 201

@app.route('/api/<queue_name>', methods=['GET'])
def get_message(queue_name):
    timeout = int(request.args.get('timeout', 10000))
    message = message_queue.dequeue(queue_name, timeout)
    
    if message is None:
        return '', 204
    
    return jsonify(message), 200

@app.route('/queue/<queue_name>', methods=['GET'])
def view_queue(queue_name):
    message = message_queue.dequeue(queue_name)
    return render_template('queue_view.html', 
                           queue_name=queue_name, 
                           message=message)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
from queues import QueueManager

app = Flask(__name__)
queue_manager = QueueManager()

# Endpoint to add a message to a queue
@app.route('/api/<queue_name>', methods=['POST'])
def add_message(queue_name):
    # Get the message from the request body in JSON format
    message = request.get_json()
    if not message:
        return jsonify({"error": "Invalid message format"}), 400
    # Add the message to the queue
    queue_manager.add_message(queue_name, message)
    return jsonify({"message": "Message added successfully"}), 200

# Endpoint to get the next message from a queue with a timeout
@app.route('/api/<queue_name>', methods=['GET'])
def get_message(queue_name):
    # Read the timeout parameter from the query string, default is 10 seconds
    timeout = int(request.args.get('timeout', 10))  
    # Retrieve the next message from the queue
    message = queue_manager.get_message(queue_name, timeout)

    if message is None:
        return '', 204  # If no message is available or timeout has expired, return 204 (No Content)

    return jsonify(message), 200  # Return the message as JSON

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app in debug mode

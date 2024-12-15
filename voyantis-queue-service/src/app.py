from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from .queue import MessageQueue

def create_app():
    """
    Create and configure the Flask application.
    
    :return: Configured Flask app
    """
    # Create Flask app with template folder in project root
    app = Flask(__name__, 
                template_folder='../../templates', 
                static_folder='../../static')
    CORS(app)
    
    # Create a global message queue instance
    message_queue = MessageQueue()

    @app.route('/')
    def index():
        """
        Render the homepage with queue statistics.
        
        :return: Rendered index template
        """
        queue_stats = message_queue.get_queue_stats()
        return render_template('index.html', queues=queue_stats)

    @app.route('/api/<queue_name>', methods=['POST'])
    def post_message(queue_name):
        """
        Add a message to a specific queue.
        
        :param queue_name: Name of the queue
        :return: JSON response with status
        """
        message = request.get_json()
        message_queue.enqueue(queue_name, message)
        return jsonify({"status": "Message enqueued"}), 201

    @app.route('/api/<queue_name>', methods=['GET'])
    def get_message(queue_name):
        """
        Retrieve a message from a specific queue.
        
        :param queue_name: Name of the queue
        :return: JSON message or 204 No Content
        """
        timeout = int(request.args.get('timeout', 10000))
        message = message_queue.dequeue(queue_name, timeout)
        
        if message is None:
            return '', 204
        
        return jsonify(message), 200

    @app.route('/queue/<queue_name>', methods=['GET'])
    def view_queue(queue_name):
        """
        View details of a specific queue.
        
        :param queue_name: Name of the queue
        :return: Rendered queue details template
        """
        message = message_queue.dequeue(queue_name)
        return render_template('queue_details.html', 
                               queue_name=queue_name, 
                               message=message)

    return app

def run():
    """
    Run the Flask application.
    """
    app = create_app()
    app.run(debug=True)

if __name__ == '__main__':
    run()

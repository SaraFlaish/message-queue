# Voyantis Queue Management Service

## Project Overview
A flexible message queue service with a REST API and web interface.

## Features
- Create multiple named queues
- Add messages to queues
- Retrieve messages with configurable timeout
- Web interface to manage queues

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip

### Installation
1. Clone the repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
```bash
python -m src.queue_service.app
```

### Running Tests
```bash
pytest tests/
```

## API Endpoints
- `POST /api/{queue_name}`: Add a message to a queue
- `GET /api/{queue_name}?timeout={ms}`: Retrieve a message from a queue

## Web Interface
Navigate to `http://localhost:5000` to view and manage queues.

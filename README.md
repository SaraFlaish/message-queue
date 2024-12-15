# Message Queue Service

## Overview
A simple message queue service with a REST API and web interface built using Python, Flask, and in-memory queue management.

## Features
- REST API for message queue management
- Web interface to view queues and their contents
- Support for multiple named queues
- Configurable timeout for message retrieval

## Prerequisites
- Python 3.8+
- pip

## Installation
1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application
```
python app.py
```

The application will be available at `http://localhost:5000`

## API Endpoints
- `POST /api/{queue_name}`: Add a message to a queue
- `GET /api/{queue_name}?timeout={ms}`: Retrieve a message from a queue

## Development
- Run tests: `python -m pytest`
- Code is formatted with Black
- Type hints used throughout

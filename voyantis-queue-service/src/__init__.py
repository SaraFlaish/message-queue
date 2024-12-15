# Initialization file for the queue service package
from .queue import MessageQueue
from .app import create_app

__all__ = ['MessageQueue', 'create_app']

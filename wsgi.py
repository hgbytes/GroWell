import os
import sys

# Add the project directory to the Python path
path = '/home/hgbytes/Gr0/Gr0'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['FLASK_APP'] = 'run.py'
os.environ['FLASK_ENV'] = 'production'

# Import the Flask application
from app import app as application 
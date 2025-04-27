from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, 
           template_folder='../templates',
           static_folder='../static')

# Configure database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '../data/plant_disease.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'plant_disease_detection_app_secret_key')

# Initialize database
db = SQLAlchemy(app)

# Initialize Socket.IO
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize chatbot
from app.chatbot import Chatbot
chatbot = Chatbot()

# Initialize Fluvio client only if available
try:
    from app.fluvio_client import FluvioClient
    fluvio_client = FluvioClient()
    app.config['FLUVIO_ENABLED'] = True
except ImportError:
    app.config['FLUVIO_ENABLED'] = False
    app.logger.warning("Fluvio streaming is not available. Some features may be limited.")

# Import routes at the end to avoid circular imports
from app import routes 
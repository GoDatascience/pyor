from flask import Flask
from flask_cors import CORS

# Flask
app = Flask(__name__)
app.config.from_object('config')
CORS(app)

# Import Controller modules explicitly
from pyor.controllers import tasks
from flask import Flask
from flask_script import Manager

from mrq import context


context.setup_context()

app = Flask(__name__)
app.config.from_object('config')

manager = Manager(app)

from mreq.controllers import index
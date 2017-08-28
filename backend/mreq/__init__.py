from flask import Flask
from flask_script import Manager
from mrq import context

# Flask
app = Flask(__name__)
app.config.from_object('config')

# MRQ
context.setup_context(file_path="workers/mrqconfig.py")

manager = Manager(app)

@manager.command
def runserver():
    app.run(host='0.0.0.0')

@manager.command
def runbot():


from mreq.controllers import tasks
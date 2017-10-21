from flask import Flask
from flask_script import Manager
from flask_cors import CORS
import mongoengine
from mrq import context

# Flask
app = Flask(__name__)
app.config.from_object('config')
CORS(app)

mongoengine.connect('pyor', host='mongodb://mongodb:27017/pyor')

manager = Manager(app)

@manager.command
def runserver():
    # MRQ
    context.setup_context(file_path="workers/mrqconfig.py")
    # workers.start_workers()
    # workers.start_workers_in_new_process("SequentialWorker", 1, "sequential")
    # workers.start_workers_in_new_process("ParallelWorker", (multiprocessing.cpu_count() - 1), "parallel")
    # Flask
    app.run(host='0.0.0.0')

from pyor.controllers import tasks
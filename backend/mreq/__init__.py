import multiprocessing
import subprocess

from flask import Flask
from flask_script import Manager

from mrq import context

# MRQ
context.setup_context()
subprocess.Popen(["mrq-worker", "--processes=1", "--name=sequential-worker", "sequential"])
subprocess.Popen(["mrq-worker", "--processes=%d" % (multiprocessing.cpu_count()-1),
                  "--name=parallel-worker", "parallel"])

# Flask
app = Flask(__name__)
app.config.from_object('config')

manager = Manager(app)

from mreq.controllers import index
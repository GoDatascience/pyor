from typing import List

import flask
from mrq.dashboard.utils import jsonify
from werkzeug.datastructures import FileStorage

from mreq import app
from mreq.models import Task

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify([task.document for task in Task.find_all()])

@app.route("/tasks", methods=["POST"])
def create_task():
    errors = []

    name: str = flask.request.form['name']
    if not name:
        errors.append({"field": "name", "message": "The name is required!"})
    if Task.exists(name):
        errors.append({"field": "name", "message": "There's already a task with this name!"})
    if "script_file" not in flask.request.files or flask.request.files["script_file"].filename == '':
        errors.append({"field": "script_file", "message": "The script file is required!"})
    if "script_file" in flask.request.files and not allowed_file(flask.request.files["script_file"].filename):
        errors.append({"field": "script_file", "message": ""})

    script_file: FileStorage = flask.request.files["script_file"]
    auxiliar_files: List[FileStorage] = flask.request.files.getlist("auxiliar_files")

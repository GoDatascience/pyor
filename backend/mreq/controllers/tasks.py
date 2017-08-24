import json
from typing import List, Dict

import flask
from mrq.dashboard.utils import jsonify
from werkzeug.datastructures import FileStorage

import mreq.services
from mreq import app
from mreq.models import Task


ALLOWED_EXTENSIONS = app.config["ALLOWED_EXTENSIONS"]
ALLOWED_SCRIPTS_EXTENSIONS = app.config["ALLOWED_SCRIPTS_EXTENSIONS"]

FIELD_NAME = "name"
FIELD_AUXILIAR_FILES = "auxiliar_files"
FIELD_SCRIPT_FILE = "script_file"
FIELD_PARAM_DEFINITIONS = "param_definitions"
FIELD_QUEUE = "queue"
FIELD_PARAMS = "params"


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify([task.document for task in Task.find_all()])


@app.route("/tasks", methods=["POST"])
def create_task():
    errors = []

    data: Dict = json.loads(flask.request.form["data"])
    name: str = data.get(FIELD_NAME)
    param_definitions: List = data.get(FIELD_PARAM_DEFINITIONS, [])

    if not name:
        errors.append({"field": FIELD_NAME, "message": "The name is required!"})
    if Task.exists(name):
        errors.append({"field": FIELD_NAME, "message": "There's already a task with this name!"})
    if FIELD_SCRIPT_FILE not in flask.request.files or flask.request.files[FIELD_SCRIPT_FILE].filename == '':
        errors.append({"field": FIELD_SCRIPT_FILE, "message": "The script file is required!"})
    if FIELD_SCRIPT_FILE in flask.request.files and not allowed_file(flask.request.files[FIELD_SCRIPT_FILE].filename):
        errors.append({"field": FIELD_SCRIPT_FILE,
                       "message": "Arquivo(s) com extensão proibida. Lista de extensões permitidas: %s"
                                  % ALLOWED_SCRIPTS_EXTENSIONS})
    if FIELD_AUXILIAR_FILES in flask.request.files and not allowed_file(flask.request.files[FIELD_AUXILIAR_FILES].filename):
        errors.append({"field": FIELD_AUXILIAR_FILES,
                       "message": "Arquivo(s) com extensão proibida. Lista de extensões permitidas: %s"
                                  % ALLOWED_EXTENSIONS})
    if param_definitions and not isinstance(param_definitions, list):
        errors.append({"field": FIELD_PARAM_DEFINITIONS, "message": "The %s must be a list!" % FIELD_PARAM_DEFINITIONS})

    if errors:
        return jsonify(errors), 400

    script_file: FileStorage = flask.request.files[FIELD_SCRIPT_FILE]
    auxiliar_files: List[FileStorage] = flask.request.files.getlist(FIELD_AUXILIAR_FILES)

    task = mreq.services.create_task(name, param_definitions, script_file, auxiliar_files)
    return jsonify(task.document), 201

@app.route("/tasks/<task_id>", methods=["PUT"])
def execute_task(task_id: str):
    errors = []

    data: Dict = flask.request.json
    queue: str = data.get(FIELD_QUEUE)
    params: Dict = data.get(FIELD_PARAMS)

    if not queue:
        errors.append({"field": FIELD_QUEUE, "message": "The queue is required!"})
    if params and not isinstance(params, dict):
        errors.append({"field": FIELD_PARAMS, "message": "The params must be a dictionary!"})

    task: Task = Task.find_one(task_id)
    if not task:
        errors.append({"field": "task_id", "message": "The task wasn't found!"})
        return jsonify(errors), 404

    if errors:
        return jsonify(errors), 400

    mreq.services.enqueue_job(task, params, queue)


def verify_extension_in_list(filename: str, list: List):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in list


def allowed_file(filename):
    return verify_extension_in_list(filename, ALLOWED_EXTENSIONS)


def allowed_script_file(filename):
    return verify_extension_in_list(filename, ALLOWED_SCRIPTS_EXTENSIONS)

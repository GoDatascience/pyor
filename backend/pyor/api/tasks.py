from typing import List, Dict

import flask
from flask.wrappers import Response
from pyor.utils import jsonify
from werkzeug.datastructures import FileStorage

import pyor.services
from pyor.api import app
from pyor.api.validations import extract_json_from_form, required_fields, validate_instance, required_files, \
    allowed_files, allowed_file_lists, filter_errors, custom_validation, extract_json
from pyor.models import Task, Queue

ALLOWED_EXTENSIONS = app.config["ALLOWED_EXTENSIONS"]
ALLOWED_SCRIPTS_EXTENSIONS = app.config["ALLOWED_SCRIPTS_EXTENSIONS"]

FIELD_NAME = "name"
FIELD_AUXILIAR_FILES = "auxiliar_files[]"
FIELD_SCRIPT_FILE = "script_file"
FIELD_PARAM_DEFINITIONS = "param_definitions"
FIELD_QUEUE = "queue"
FIELD_PARAMS = "params"


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(items=[task.to_mongo() for task in Task.objects])


@app.route("/tasks", methods=["POST"])
@extract_json_from_form("data")
@required_fields(FIELD_NAME)
@validate_instance(FIELD_PARAM_DEFINITIONS, list)
@required_files(FIELD_SCRIPT_FILE)
@allowed_files(ALLOWED_SCRIPTS_EXTENSIONS, FIELD_SCRIPT_FILE)
@allowed_file_lists(ALLOWED_EXTENSIONS, FIELD_AUXILIAR_FILES)
@filter_errors
def create_task(data: Dict= None):
    name: str = data.get(FIELD_NAME)
    param_definitions: List = data.get(FIELD_PARAM_DEFINITIONS, [])
    script_file: FileStorage = flask.request.files[FIELD_SCRIPT_FILE]
    auxiliar_files: List[FileStorage] = flask.request.files.getlist(FIELD_AUXILIAR_FILES)

    task = pyor.services.create_task(name, param_definitions, script_file, auxiliar_files)

    return jsonify(task.to_mongo()), 201

@app.route("/tasks/<task_id>", methods=["PUT"])
@extract_json
@required_fields(FIELD_QUEUE)
@validate_instance(FIELD_PARAMS, dict)
@filter_errors
def execute_task(task_id: str, data: Dict= None):
    queue: str = data.get(FIELD_QUEUE)
    params: Dict = data.get(FIELD_PARAMS)
    if not params:
        params = {}

    task: Task = Task.objects(pk=task_id).first()
    if not task:
        return jsonify(errors=[{"field": "task_id", "message": "The task wasn't found!"}]), 404

    pyor.services.enqueue_job(task, params, Queue.objects.get(name=queue))
    return Response(status=200)
import json
from functools import wraps
from typing import Dict, Type, List, Callable

import flask

def extract_json(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data: Dict = flask.request.json
        kwargs["data"] = data
        return func(*args, **kwargs)
    return wrapper

def extract_json_from_form(field: str):
    def extract_json_from_form_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data: Dict = json.loads(flask.request.form[field])
            kwargs["data"] = data
            return func(*args, **kwargs)
        return wrapper
    return extract_json_from_form_decorator

def required_fields(*fields: str):
    def required_fields_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            errors = get_errors(kwargs)
            data: Dict = kwargs["data"]
            for field in fields:
                if field not in data:
                    errors.append({"field": field, "message": "Field is required!"})
            return func(*args, **kwargs)
        return wrapper
    return required_fields_decorator

def validate_instance(field: str, type: Type):
    def validate_instance_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            errors = get_errors(kwargs)
            data: Dict = kwargs["data"]
            if field in data and not isinstance(data[field], type):
                errors.append({"field": field, "message": "Must be a %s!" % type.__name__})
            return func(*args, **kwargs)
        return wrapper
    return validate_instance_decorator

def required_files(*fields: str):
    def required_files_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            errors = get_errors(kwargs)
            for field in fields:
                if field not in flask.request.files or flask.request.files[field].filename == '':
                    errors.append({"field": field, "message": "File is required!"})
            return func(*args, **kwargs)
        return wrapper
    return required_files_decorator


def allowed_files(allowed_extensions: List, *fields: str):
    def allowed_files_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            errors = get_errors(kwargs)
            for field in fields:
                if field in flask.request.files and not verify_extension_in_list(
                        flask.request.files[field].filename, allowed_extensions):
                    errors.append({"field": field,
                                   "message": "File extension not allowed. List of allowed extensions: %s"
                                              % allowed_extensions})
            return func(*args, **kwargs)
        return wrapper
    return allowed_files_decorator


def allowed_file_lists(allowed_extensions: List, *fields: str):
    def allowed_files_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            errors = get_errors(kwargs)
            for field in fields:
                if field in flask.request.files:
                    file_list = flask.request.files.getlist(field)
                    for i, file in enumerate(file_list):
                        if not verify_extension_in_list(file.filename, allowed_extensions):
                            errors.append({"field": "%s[%d]" % (field, i),
                                           "message": "File extension not allowed. List of allowed extensions: %s"
                                                      % allowed_extensions})
            return func(*args, **kwargs)
        return wrapper
    return allowed_files_decorator


def custom_validation(field: str, validation_function: Callable, message: str):
    def custom_validation_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            errors = get_errors(kwargs)
            data: Dict = kwargs["data"]
            if not validation_function(data.get(field)):
                errors.append({"field": field, "message": message})
            return func(*args, **kwargs)
        return wrapper
    return custom_validation_decorator


def filter_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        errors = get_errors(kwargs)
        if errors:
            return flask.jsonify(errors=errors), 400
        del kwargs["errors"]
        return func(*args, **kwargs)
    return wrapper


def get_errors(kwargs: Dict):
    errors = kwargs.get("errors", [])
    kwargs["errors"] = errors
    return errors

def verify_extension_in_list(filename: str, list: List):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in list
from typing import Dict, List

from flask_security.utils import hash_password

from pyor.api import app
from pyor.api.auth import user_registered_callback
from pyor.models import User
from pyor.services import enqueue_experiment


def experiment_inserted_callback(experiments: List[Dict]):
    for experiment in experiments:
        enqueue_experiment(experiment["_id"])

def before_user_registered_callback(users: List[Dict]):
    for user in users:
        user['password'] = hash_password(user['password'])

def after_user_registered_callback(users: List[Dict]):
    for user in users:
        user_registered_callback(User.objects.get(id=user["_id"]))

def before_get_users_callback(response: Dict):
    for doc in response['_items']:
        doc.pop("password")

def before_get_user_callback(doc: Dict):
    doc.pop("password")

app.on_inserted_experiment += experiment_inserted_callback
app.on_insert_user += before_user_registered_callback
app.on_inserted_user += after_user_registered_callback
app.on_fetched_resource_user += before_get_users_callback
app.on_fetched_item_user += before_get_user_callback
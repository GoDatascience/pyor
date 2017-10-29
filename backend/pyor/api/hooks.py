from typing import Dict, List

from pyor.api import app
from pyor.services import enqueue_experiment


def experiment_inserted_callback(experiments: List[Dict]):
    for experiment in experiments:
        enqueue_experiment(experiment["_id"])


app.on_inserted_experiment += experiment_inserted_callback
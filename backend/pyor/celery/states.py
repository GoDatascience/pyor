from celery.states import *

PROGRESS = "PROGRESS"

UNREADY_STATES = frozenset({*UNREADY_STATES, PROGRESS})
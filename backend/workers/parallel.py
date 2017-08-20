import multiprocessing

from workers.mrqconfig import *

NAME = "parallel"
QUEUES = ("parallel",)
PROCESSES = multiprocessing.cpu_count()
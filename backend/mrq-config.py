""" Redis and MongoDB settings
"""
#MongoDB settings
MONGODB_JOBS = "mongodb://127.0.0.1:27017/mrq" # MongoDB URI for the jobs, scheduled_jobs & workers database.Defaults to mongodb://127.0.0.1:27017/mrq

#Redis settings
REDIS = "redis://127.0.0.1:6379"

"""General MrQ settings
"""
WORKER_CLASS = "mrq.worker.Worker"
DEFAULT_JOB_TIMEOUT = 2*24*60*60 # 2 days

""" mrq-worker settings
"""
MAX_MEMORY = -1
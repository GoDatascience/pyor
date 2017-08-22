from typing import Dict

from mrq import context


def run(params: Dict):
    n = params["n"]
    slow_fib(n)

def slow_fib(n):
    context.set_current_job_progress(1 / (n if n > 0 else 1))
    if n <= 1:
        return 1
    else:
        return slow_fib(n-1) + slow_fib(n-2)
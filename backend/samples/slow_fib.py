from typing import Dict


def run(self, params: Dict):
    n = params["n"]
    return slow_fib(self, n)

def slow_fib(self, n):
    if n <= 1:
        return 1
    else:
        self.update_progress(1 / (n if n > 0 else 1))
        return slow_fib(self, n-1) + slow_fib(self, n-2)
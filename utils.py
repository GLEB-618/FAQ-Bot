import time

class Timer:
    def __init__(self, label: str ="⏱"):
        self.label = label
        self.elapsed = 0

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.elapsed = time.perf_counter() - self.start
        print(f"[Timer] {self.label} — {self.elapsed:.3f} сек")
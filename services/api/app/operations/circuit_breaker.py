# Circuit Breaker & Graceful Degradation Engine

import time
from typing import Dict, Any, Callable

class CircuitBreaker:
    """Protects external dependencies (AI providers, OCR engines) via threshold-based tripmeter & fallback states."""

    def __init__(self, failure_threshold: int = 3, reset_timeout_sec: int = 30):
        self.failure_threshold = failure_threshold
        self.reset_timeout_sec = reset_timeout_sec
        self.failure_count = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.last_state_change = time.time()

    def execute(self, func: Callable, fallback_func: Callable, *args, **kwargs) -> Any:
        now = time.time()

        if self.state == "OPEN":
            if now - self.last_state_change > self.reset_timeout_sec:
                self.state = "HALF_OPEN"
                self.last_state_change = now
            else:
                return fallback_func(*args, **kwargs)

        try:
            result = func(*args, **kwargs)
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
                self.last_state_change = now
            return result
        except Exception as err:
            self.failure_count += 1
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                self.last_state_change = now
            return fallback_func(*args, **kwargs)

circuit_breaker = CircuitBreaker()

import socket
from contextlib import closing
from typing import Tuple


def ping_host(host: str, timeout: int = 3) -> Tuple[bool, float]:
    """Attempt to connect to host:80 to approximate reachability, returns (reachable, ms)."""
    try:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            sock.settimeout(timeout)
            import time
            start = time.perf_counter()
            sock.connect((host, 80))
            duration = (time.perf_counter() - start) * 1000.0
            return True, duration
    except Exception:
        return False, 0.0

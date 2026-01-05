import time
import requests

def check_website(url: str, timeout: int = 10):
    start = time.time()
    try:
        response = requests.get(url, timeout=timeout)
        response_time = time.time() - start

        return {
            "status_code": response.status_code,
            "response_time": response_time,
            "is_up": response.status_code < 500
        }
    except requests.RequestException:
        return {
            "status_code": None,
            "response_time": None,
            "is_up": False
        }

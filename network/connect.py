"""
    A function that makes a GET request and returns a ``Response`` object.

    **Author:** JuaanReis 
    **Date:** 25-05-2027        
    **Last modification:** -         
    **E-mail:** teixeiradosreisjuan@gmail.com           
    **Version:** 1.6.2

    **Example:**
        ```python
        from network.connect import get_response
        url = "https://example.com/"
        response = get_response(url)
        print(response.text)
        ```
"""

from httpx import HTTPStatusError, ConnectError, RequestError, Response
from network.config_net import clients
from time import sleep
import config

def get_response(url: str, retries: int = 3, delay: float = config.delay) -> Response | None:

    rr = 0  

    for attempt in range(retries):

        c = clients[rr % len(clients)]
        rr += 1

        try:
            response = c.get(url)
            response.raise_for_status()
            return response

        except HTTPStatusError as e:
            status = e.response.status_code

            if status == 429:
                retry_after = int(e.response.headers.get("Retry-After", 1))
                sleep(retry_after)
                continue

            return None

        except (ConnectError, RequestError):
            sleep(delay * (1 + attempt * 0.5))
            continue

        except Exception:
            sleep(delay * (1 + attempt * 0.5))
            continue

    return None
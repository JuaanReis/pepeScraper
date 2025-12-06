"""
    Functions that search and return all 4chan boards, ensuring the project
    does not use deprecated boards and none are left out.

    **Author:** JuaanReis       
    **Date:** 28-08-2025        
    **Last modification:** 21-11-2025         
    **E-mail:** teixeiradosreisjuan@gmail.com           
    **Version:** 1.1.5        

    **Example:**
        ```python
    from get_all_boards import get_boards_api

    boards = get_boards_api()

    for board in boards:
        print(board)
        ```
"""

from httpx import Response, HTTPStatusError, ConnectError, RequestError
import orjson as json
import config
from time import sleep, time

def get_response(url: str, retries: int = 3, delay: float = config.delay):

    rr = 0  

    for attempt in range(retries):

        c = config.clients[rr % len(config.clients)]
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

def get_boards_api() -> dict:
    start = time()
    boards = get_response("https://a.4cdn.org/boards.json")
    if not boards:
        print("ERROR: could not access the api.")
        if config.debug and boards is not None:
            print(f"[API STATUS] {boards.status_code}")
        return

    data = json.dumps(
        boards.json(),
        option=json.OPT_INDENT_2 
    )

    with open("./src/data/boards.json", "wb") as f:
        f.write(data)

    end = time()

    return boards.json()

if config.auto_update:
    get_boards_api()
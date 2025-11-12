"""
    Functions that search and return all 4chan boards, ensuring the project
    does not use deprecated boards and none are left out.

    **Author:** JuaanReis       
    **Date:** 28-08-2025        
    **Last modification:** 12-11-2025       
    **E-mail:** teixeiradosreisjuan@gmail.com           
    **Version:** 1.1.3b3        

    **Example:**
        ```python
    from get_all_boards import get_boards_api

    boards = get_boards_api()

    for board in boards:
        print(board)
        ```
"""

import httpx
import json
import config
import time

client = httpx.Client(http2=True, timeout=httpx.Timeout(10.0, connect=5.0))

def get_response(url: str, retries: int = 3, delay: float = 1.0) -> httpx.Response | None:
    for attempt in range(retries):
        try:
            response = client.get(url)
            response.raise_for_status()
            return response

        except httpx.ConnectError as e:
            if "10035" in str(e):
                if config.debug:
                    print(f"[SOCKET BUSY] {url} -> retry {attempt+1}/{retries} in {delay}s")
                time.sleep(delay)
                continue
            if config.debug:
                print(f"[CONNECT ERROR] {url} -> {e}")
            time.sleep(delay)
            continue

        except httpx.RequestError as e:
            if config.debug:
                print(f"[REQUEST ERROR] {url} -> {e}")
            time.sleep(delay)
            continue

        except httpx.HTTPStatusError as e:
            if config.debug:
                print(f"[HTTP STATUS ERROR] {url} -> {e.response.status_code}")
            return None

        except Exception as e:
            if config.debug:
                print(f"[UNEXPECTED ERROR] {url} -> {e}")
            time.sleep(delay)
            continue

    if config.debug:
        print(f"[FAILED AFTER RETRIES] {url}")
    return None

def get_boards_api() -> list:
    boards = get_response("https://a.4cdn.org/boards.json")
    if not boards:
        print("ERROR: could not access the api.")
        if config.debug:
            print(f"[API STATUS] {boards.status_code}")
        return
    with open("./src/data/boards.json", "w") as f:
        json.dump(boards.json(), f, indent=4)
    
    return boards.json()
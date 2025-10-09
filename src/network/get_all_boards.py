"""
    Functions that search and return all 4chan boards, ensuring the project
    does not use deprecated boards and none are left out.

    **Author:** JuaanReis       
    **Date:** 28-08-2025        
    **Last modification:** 25-09-2025       
    **E-mail:** teixeiradosreisjuan@gmail.com           
    **Version:** 1.1.3b2        

    **Example:**
        ```python
    from get_all_boards import get_boards_api

    boards = get_boards_api()

    for board in boards:
        print(board)
        ```
"""

import httpx
from httpx import Response
import json
import config

client = httpx.Client(http2=True, timeout=httpx.Timeout(5.0, connect=2.0))

def get_response(url: str) -> httpx.Response | None:
    try:
        response = client.get(url)
        response.raise_for_status()  
        return response
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        if config.debug:
            print(f"[HTTP ERROR] {url} -> {e}")
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
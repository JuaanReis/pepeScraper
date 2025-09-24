"""
    Functions that search and return all 4chan boards, ensuring the project
    does not use deprecated boards and none are left out.

    Author: JuaanReis
    Date: 28-08-2025
    Last modification: 24-09-2025
    E-mail: teixeiradosreisjuan@gmail.com   
    Version: 0.0.1

    Example:
        from get_all_boards import get_boards_api

        boards = get_boards_api()

        for board in boards:
            print(board)
"""

import httpx
from httpx import Response
from src.utils.load_config import load_config_json
import json

def get_response(url: str) -> Response | None:
    try:
        DATA = load_config_json()
        with httpx.Client(http2=True) as client:
            response = client.get(url, timeout=4)
        return response
    except httpx.RequestError:
        return None

def get_boards_api() -> list:
    boards = get_response("https://a.4cdn.org/boards.json")
    if not boards:
        print("ERROR: could not access the api.")
        return
    with open("./src/data/boards.json", "w") as f:
        json.dump(boards.json(), f, indent=4)
    
    return boards.json()
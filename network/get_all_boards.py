"""
    Functions that search and return all 4chan boards, ensuring the project
    does not use deprecated boards and none are left out.

    **Author:** JuaanReis       
    **Date:** 28-08-2025        
    **Last modification:** 25-05-2026         
    **E-mail:** teixeiradosreisjuan@gmail.com           
    **Version:**  1.1.5rc2       

    **Example:**
        ```python
    from get_all_boards import get_boards_api
  
    boards = get_boards_api()

    for board in boards:
        print(board)
        ```
"""

import orjson as json
import config
from network.connect import get_response

def get_boards_api() -> dict:
    boards = get_response("https://a.4cdn.org/boards.json")
    if not boards:
        print("[ERROR] could not access the api.")
        if config.debug and boards is not None:
            print(f"[API STATUS] {boards.status_code}")
        return

    data = json.dumps(
        boards.json(),
        option=json.OPT_INDENT_2 
    )

    with open("./data/boards.json", "wb") as f:
        f.write(data)

    return boards.json()

if config.auto_update:
    get_boards_api()
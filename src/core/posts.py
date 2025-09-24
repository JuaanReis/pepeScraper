"""
    Function that lists the threads and makes a request to find the post information.

    Author: JuaanReis
    Date: 24-09-2025
    Last modification: -
    E-mail: teixeiradosreisjuan@gmail.com
    Version: 0.0.1

    Example:
        from src.core.posts import ...
"""
import json
from src.network.get_all_boards import get_response

def get_post() -> list:
    try:
        with open("./src/data/boards.json", "r") as f:
            data = json.load(f)
        return [board["board"] for board in data["boards"]]
    except FileNotFoundError:
        return []
    
def get_post_thread() -> dict:
    boards = get_post()
    all_threads = {}
    for b in boards:
        response = get_response(f"https://a.4cdn.org/{b}/catalog.json")
        if response:
            catalog = response.json()
            threads = []
            for page in catalog:
                for thread in page.get("threads", []):
                    threads.append(thread["no"])
    all_threads[b] = threads

    return all_threads, catalog

def save_thread(threads: dict):
    with open("./src/data/threads.json", "w") as f:
        json.dump(threads, f)

def get_thread_info(board: str, thread_no: int) -> dict | None:
    response = get_response(f"https://a.4cdn.org/{board}/thread/{thread_no}.json")
    if response:
        return response.json()
    else:
        return None
"""
    Function that lists the threads and makes a request to find the post information.

    **Author:** JuaanReis       
    **Date:** 24-09-2025        
    **Last modification:** 08-10-2025       
    **E-mail:** teixeiradosreisjuan@gmail.com       
    **Version:** 1.1.3b2        

    **Example:**
        ```python
    from src.core.posts import save_threads, get_post_thread

    threads_dict = get_post_thread()
    save_threads(threads_dict)
        ```
"""
import json
from src.network.get_all_boards import get_response
from concurrent.futures import ThreadPoolExecutor
import config
from tqdm import tqdm

def get_post() -> list:
    try:
        with open("./src/data/boards.json", "r") as f:
            data = json.load(f)
        return [board["board"] for board in data["boards"]]
    except FileNotFoundError as e:
        if config.debug:
            print(f"[ERROR FILE POST]: {e}")
        return []
    
def get_post_thread(selected_boards: list[str] | None = None) -> dict:
    boards = get_post()

    if selected_boards:
        boards = [b for b in boards if b in selected_boards]

    all_threads = {}

    def fetch_boards(b):
        api_url = f"https://a.4cdn.org/{b}/catalog.json"
        response = get_response(api_url)
        if config.debug:
            print(f"[REQUEST API] In {api_url}")

        if not response:
            if config.debug:
                print(f"[ERROR RESPONSE API] No response from {api_url}")
            return b, []

        try:
            catalog = response.json()
        except ValueError:
            if config.debug:
                print(f"[ERROR JSON API] Invalid JSON {api_url}")
            return b, []

        threads = [thread["no"] for page in catalog for thread in page.get("threads", [])]

        if config.debug:
            print(f"[NUMBER OF THREADS] {len(threads)} in {b}")

        return b, threads

    with ThreadPoolExecutor(max_workers=30) as executor:
        results = list(executor.map(fetch_boards, tqdm(boards, desc="Processing boards", ncols=100)))

    for b, threads in results:
        all_threads[b] = threads

    return all_threads

def save_threads(threads: dict):
    with open("./src/data/threads.json", "w") as f:
        json.dump(threads, f, indent=4)

def get_thread_info(board: str, thread_no: int) -> dict | None:
    api_url = f"https://a.4cdn.org/{board}/thread/{thread_no}.json"
    response = get_response(api_url)
    if config.debug:
        print(f"[RESPONSE STATUS API] {api_url}")
    if response and response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            if config.debug:
                print(f"[ERROR JSON API] It's not JSON: {api_url}")
            return None
    else:
        if config.debug:
            print("[THREAD ERROR] Not response")
        return None
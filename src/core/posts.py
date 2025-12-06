"""
    Function that returns all threads and their information.

    **Author:** JuaanReis           
    **Date:** 25-09-2025            
    **Last modification:** 21-11-2025             
    **E-mail:** teixeiradosreisjuan@gmail.com           
    **Version:** 1.1.5            

    **Example:**
        ```python
    from src.core.post import get_post_thread
    threads_data = get_post_thread(board_args)
        ```
"""
import orjson as json
from src.network.get_all_boards import get_response, get_boards_api
from concurrent.futures import ThreadPoolExecutor
import config
from tqdm import tqdm
tqdm._instances.clear()

def get_post() -> list:
    # Tenta ler as boards
    try:
        with open("./src/data/boards.json", "r") as f:
            data = json.loads(f.read())
        return [board["board"] for board in data["boards"]]

    except (FileNotFoundError, json.JSONDecodeError):
        boards = get_boards_api()  

        if not boards:
            raise RuntimeError("Failed to download boards: get_boards_api() returned empty." if config.debug else "")

        try:
            with open("./src/data/boards.json", "r") as f:
                data = json.loads(f.read())
            return [board["board"] for board in data["boards"]]

        except Exception as e:
            raise RuntimeError(f"Boards.json still invalid after recreation: {e}")

def get_post_thread(selected_boards: list[str] | None = None, workers=20) -> dict:
    boards = get_post()

    if selected_boards:
        selected = set(selected_boards)
        boards = [b for b in boards if b in selected]

    all_threads = {}

    def fetch_boards(b):
        api_url = f"https://a.4cdn.org/{b}/catalog.json"

        if config.debug:
            print(f"[REQUEST API] {api_url}")

        response = get_response(api_url, 2, 0.5)

        if not response:
            if config.debug:
                print(f"[ERROR RESPONSE API] No response from {api_url}")
            return (b, ())

        try:
            catalog = json.loads(response.content)
        except ValueError:
            if config.debug:
                print(f"[ERROR JSON API] Invalid JSON {api_url}")
            return (b, ())

        threads = tuple(thread["no"]
                        for page in catalog
                        for thread in page.get("threads", []))

        return (b, threads)

    boards_iter = tqdm(boards, desc="Processing boards", bar_format=config.color_ansi + "{l_bar}{bar}{r_bar}" + "\033[0m", ncols=100) if not config.debug else boards

    max_workers = min(workers, config.max_threads * config.thread_multiplier)

    with ThreadPoolExecutor(max_workers=max_workers) as exe:
        for b, threads in exe.map(fetch_boards, boards_iter):
            all_threads[b] = threads

    return all_threads

def save_threads(threads: dict):
    with open("./src/data/threads.json", "w") as f:
        json.dump(threads, f, indent=4)

def get_thread_info(board: str, thread_no: int) -> dict | None:
    api_url = f"https://a.4cdn.org/{board}/thread/{thread_no}.json"
    response = get_response(api_url)
    if config.debug:
        tqdm.write(f"[RESPONSE STATUS API] {api_url}")

    if response and response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            if config.debug:
                tqdm.write(f"[ERROR JSON API] Not valid JSON: {api_url}")
            return None
    else:
        if config.debug:
            tqdm.write("[THREAD ERROR] No response")
        return None
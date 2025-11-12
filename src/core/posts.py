import json
from src.network.get_all_boards import get_response
from concurrent.futures import ThreadPoolExecutor
import config
from tqdm import tqdm

tqdm._instances.clear()

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
            tqdm.write(f"[REQUEST API] {api_url}")

        if not response:
            if config.debug:
                tqdm.write(f"[ERROR RESPONSE API] No response from {api_url}")
            return b, []

        try:
            catalog = response.json()
        except ValueError:
            if config.debug:
                tqdm.write(f"[ERROR JSON API] Invalid JSON {api_url}")
            return b, []

        threads = [thread["no"] for page in catalog for thread in page.get("threads", [])]

        if config.debug:
            tqdm.write(f"[THREAD COUNT] {len(threads)} in {b}")

        return b, threads

    boards_iter = boards if config.debug else tqdm(boards, desc="Processing boards", ncols=100)

    with ThreadPoolExecutor(max_workers=30) as executor:
        results = list(executor.map(fetch_boards, boards_iter))

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
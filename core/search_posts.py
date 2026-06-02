"""
    Functions that search for the term passed by the user in a context on 4chan.

    **Author:** JuaanReis       
    **Date:** 25-09-2025        
    **Last modification:** 25-12-2025          
    **E-mail:** teixeiradosreisjuan@gmail.com       
    **Version:**  1.1.5rc2           

    **Example:**
        ```python
    from core.search_post import search_threads
    result = search_threads(args)
        ```
"""
from core.posts import get_post_thread
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.matcher import thread_matches
from core.cache import get_thread_info_cached
from argparse import Namespace
from tqdm import tqdm
import config

def search_threads(args: Namespace) -> dict:
    board_args = args.board if args.board else None
    threads_data = get_post_thread(board_args, args.threads)
    results = {}
    tasks = []

    if args.board:
        boards = {b: threads_data.get(b, []) for b in args.board}
    else:
        boards = threads_data

    for board, thread_list in boards.items():
        for thread_no in thread_list:
            tasks.append((board, thread_no))

    total_tasks = len(tasks)
    if total_tasks == 0:
        return results
    
    threads = min(args.threads, config.max_threads)
    with ThreadPoolExecutor(max_workers=threads * max(1, config.thread_multiplier)) as executor:
        futures = {
            executor.submit(get_thread_info_cached, board, thread_no): (board, thread_no)
            for board, thread_no in tasks
        }

        if args.live:
            iterator = as_completed(futures)
        else:
            iterator = tqdm(
                as_completed(futures),
                mininterval=config.update_bar,
                total=total_tasks,
                desc="Processing threads"
            )

        if args.live:
            print("\n" + "--" * 20)

        for future in iterator:
            board, thread_no = futures[future]

            try:
                thread_info = future.result()
            except Exception:
                continue
            
            if not thread_info:
                continue
            
            if thread_matches(thread_info, args):
                results.setdefault(board, []).append(thread_no)

                if args.live:
                    first_post = thread_info["posts"][0]

                    title = first_post.get("sub", "[No title]")

                    print(
                        f"[{board}] "
                        f"https://boards.4chan.org/{board}/thread/{thread_no} "
                        f"→ {title}"
                    )

    return results

def build_thread_links(results: dict) -> dict:
    links = {board: [] for board in results}

    tasks = [
        (board, thread_no)
        for board, thread_list in results.items()
        for thread_no in thread_list
    ]

    def fetch(board, thread_no):
        url = f"https://boards.4chan.org/{board}/thread/{thread_no}"
        info = get_thread_info_cached(board, thread_no)

        if not info or "posts" not in info or not info["posts"]:
            return board, {"url": url, "title": "[No title]", "comment": "[No content]"}

        first_post = info["posts"][0]
        title = first_post.get("sub", "[No title]")
        comment = first_post.get("com", "").replace("<br>", "\n").replace("<wbr>", "").strip()
        if len(comment) > 150:
            comment = comment[:150] + "..."

        return board, {"url": url, "title": title, "comment": comment}

    with ThreadPoolExecutor(max_workers=config.max_threads) as executor:
        futures = {executor.submit(fetch, board, thread_no): (board, thread_no) for board, thread_no in tasks}
        for future in as_completed(futures):
            try:
                board, entry = future.result()
                links[board].append(entry)
            except Exception:
                continue

    return links

def save_links(links: dict, file: str):
    try:
        if file == None:
            return
        with open(file, "w", encoding="utf-8") as f:
            for board, link_list in links.items():
                f.write(f"[Board {board}]\n")
                f.write("---------\n")
                for link in link_list:
                    f.write(f"{link}\n")
                f.write("\n")
        print(f"Results saved in {file}")
    except Exception as e:
        if config.debug:
            print(f"[ERROR SAVE RESULT]: {e}")
"""
    Functions that search for the term passed by the user in a context on 4chan.

    **Author:** JuaanReis       
    **Date:** 25-09-2025        
    **Last modification:** 10-11-2025        
    **E-mail:** teixeiradosreisjuan@gmail.com       
    **Version:** 1.1.3b3            

    **Example:**
        ```python
    from src.core.search_post import search_threads
    result = search_threads(args)
        ```
"""
from src.core.posts import get_post_thread, get_thread_info
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.core.matcher import thread_matches
from argparse import Namespace
from tqdm import tqdm
from config import debug

def search_threads(args: Namespace) -> dict:
    board_args = args.board if args.board else None
    threads_data = get_post_thread(board_args)
    results = {}
    tasks = []

    if args.board:
        boards = {b: threads_data.get(b, []) for b in args.board}
    else:
        boards = threads_data

    for board, thread_list in boards.items():
        if args.thread:
            if args.thread in thread_list:
                tasks.append((board, args.thread))
            else:
                continue
        else:
            for thread_no in thread_list:
                tasks.append((board, thread_no))

    total_tasks = len(tasks)
    if total_tasks == 0:
        return results

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {executor.submit(get_thread_info, board, thread_no): (board, thread_no) for board, thread_no in tasks}

        for future in tqdm(as_completed(futures), total=total_tasks, desc="Processing threads", ncols=100):
            board, thread_no = futures[future]
            try:
                thread_info = future.result()
            except Exception:
                continue

            if not thread_info:
                continue

            if thread_matches(thread_info, args):
                if board not in results:
                    results[board] = []
                results[board].append(thread_no)

    return results

from src.core.posts import get_thread_info

def build_thread_links(results: dict) -> dict:
    links = {}

    for board, thread_list in results.items():
        links[board] = []
        for thread_no in thread_list:
            url = f"https://boards.4chan.org/{board}/thread/{thread_no}"

            info = get_thread_info(board, thread_no)
            if not info or "posts" not in info or not info["posts"]:
                links[board].append({"url": url, "title": "[No title]", "comment": "[No content]"})
                continue

            first_post = info["posts"][0]
            title = first_post.get("sub", "[No title]")
            comment = first_post.get("com", "").replace("<br>", "\n").replace("<wbr>", "").strip()

            if len(comment) > 150:
                comment = comment[:150] + "..."

            links[board].append({
                "url": url,
                "title": title,
                "comment": comment
            })

    return links

def save_links(links: dict, file: str):
    try:
        with open(file, "w", encoding="utf-8") as f:
            for board, link_list in links.items():
                f.write(f"[Board {board}]\n")
                f.write("---------\n")
                for link in link_list:
                    f.write(f"{link}\n")
                f.write("\n")
        print("...")
    except Exception as e:
        if debug:
            print(f"[ERROR SAVE RESULT]: {e}")
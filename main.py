from src.output.banner import banner_info, display_links
from src.output.boards_helper import print_boards
from src.core.search_posts import search_threads, build_thread_links, save_log
from src.core.output import download_output
from src.flags import parse_args
from src.utils.color import colorize
from config import auto_cls 
from time import time

def main():
    start_run = time()
    args = parse_args()
    if args.all_boards:
        print_boards()
    banner_info()
    start = time()
    results = search_threads(args)
    end = time()
    links = build_thread_links(results)
    save_log(links, args)
    display_links(links, args)
    download_output(args, links, results)
    end_run = time()
    print("--" * 20)
    print(f"Requests made in {colorize(f"{end - start:.2f}s", "\033[33m")}")
    print(f"Task completed in {colorize(f"{end_run - start_run:.2f}s", "\033[33m")}")

if __name__ == "__main__":
    if auto_cls:
        from os import system
        system('cls')
    main()
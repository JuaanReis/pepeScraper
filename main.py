from output.banner import banner_info, display_links
from output.boards_helper import print_boards
from core.search_posts import search_threads, build_thread_links
from core.save_log import save_log
from core.output import download_output
from output.color import colorize
from config import auto_cls 
from time import time
from pepescraper.args import args

def main():
    start_run = time()
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
    print(f"Requests made in {colorize(f'{end - start:.3f}s', "\033[33m")}")
    print(f"Task completed in {colorize(f'{end_run - start_run:.3f}s', "\033[33m")}")

if __name__ == "__main__":
    if auto_cls:
        from os import system, name
        system('cls' if name == 'nt' else 'clear')
    try:
        from sys import exit
        main()
    except (KeyboardInterrupt, EOFError, ValueError):
        exit(0)
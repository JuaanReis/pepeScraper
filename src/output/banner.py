""" 
    Function for styling and information on the use of the program when running it. 

    **Author:** JuaanReis       
    **Date:** 25-09-2025        
    **Last modification:** 21-11-2025       
    **E-mail:** teixeiradosreisjuan@gmail.com       
    **Version:** 1.1.6            

    **Example:**        
    ```python
        from output.banner import banner_info
    
        banner_info()
    ```
"""

from argparse import Namespace
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, init
from os import cpu_count
from src.flags import parse_args
from src.utils.color import colorize
from config import logo, output_print, color_ansi

init(autoreset=True)

nsfw_boards = [
    "h", "e", "u", "d", "s", "hc", "hm", "y", "t",
    "gif", "r", "hr", "i", "aco"
]

def banner_logo() -> str:
    if logo:
        with open("./src/output/banner.txt", "r") as f:
            return f.read()
    return ""

def print_line(msg: str, size: int = 10, banner: str = ""):
    print("_" * size, msg, "_" * size)
    print(banner)
    print()

    args = parse_args()
    args_dict = vars(args)

    max_len = max(len(flag) for flag in args_dict.keys())

    print("‾" * ((size * 2) + len(msg) + 2))

    for flag, value in args_dict.items():
        if value is not None:
            print(f"  {colorize("$", Fore.GREEN)} {flag.ljust(max_len)} : {color_ansi}{value}\033[0m")

    print()
    print("‾" * ((size * 2) + len(msg) + 2))

def banner_info():
    if output_print:
        with open("./src/output/version.txt", "r") as f:
            version = f.read().strip()

        print_line(
            colorize(f"pepeScraper {version} ", Fore.GREEN),
            35,
            colorize(banner_logo(), "\033[37m")
        )

def process_thread(board, thread, args) -> str:
    url = thread.get("url", "unknown")

    if board in nsfw_boards and not args.nsfw_title:
        title = colorize("[Title blocked on NSFW boards]", Fore.RED)
    else:
        title = thread.get("title", "Title not found")

    return (
        f"{colorize('[+]', Fore.GREEN)} "
        f"{colorize(url, Fore.YELLOW)} → "
        f"{colorize(title, Fore.MAGENTA if not board in nsfw_boards else Fore.RED)}"
    )

def display_links(links: dict, args: Namespace):
    max_threads = min(args.threads, cpu_count() * 5)

    for board, thread_links in links.items():
        print()

        if output_print:
            print(
                f"{colorize(f'[Board {board}]', Fore.CYAN)} → "
                f"{colorize(str(len(thread_links)), Fore.YELLOW)} results"
            )
            print("-" * (8 + len(board)))

        if not thread_links:
            print(colorize("[-] Link not found", Fore.RED))
            print()
            continue

        results = []

        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = {
                executor.submit(process_thread, board, thread, args): thread
                for thread in thread_links
            }

            for fut in as_completed(futures):
                results.append(fut.result())

        for line in results:
            print(line)

        print()

if __name__ == "__main__":
    banner_info()
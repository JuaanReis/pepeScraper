""" 
    Function for styling and information on the use of the program when running it. 

    **Author:** JuaanReis       
    **Date:** 25-09-2025        
    **Last modification:** 25-12-2025       
    **E-mail:** teixeiradosreisjuan@gmail.com       
    **Version:** 1.1.5rc2            

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
        s_logo = colorize("The logo took a day off (or maybe it's just not coming back).", "\033[41m")
        try:
            with open("./src/output/banner.txt", "r") as f:
                return f.read() or s_logo
        except FileNotFoundError:
            return s_logo
    return ""

def print_line(msg: str, size: int = 10, banner: str = ""):
    total_width = (size * 2) + len(msg) + 2

    print("_" * size, msg, "_" * size)

    if banner:
        lines = banner.splitlines()

        non_empty = [l for l in lines if l.strip()]

        min_indent = min(len(l) - len(l.lstrip()) for l in non_empty)

        normalized = [l[min_indent:] for l in lines]

        max_banner_width = max(len(l) for l in normalized)

        block_pad = max(0, (total_width - max_banner_width) // 2)

        for line in normalized:
            print(" " * block_pad + line)

    print()

    args = parse_args()
    args_dict = vars(args)

    max_len = max(len(flag) for flag in args_dict.keys())

    print("‾" * total_width)

    for flag, value in args_dict.items():
        if value not in (None, "", False):
            if isinstance(value, list):
                value_str = ", ".join(str(v) for v in value)
            else:
                value_str = str(value)

            print(
                f"  {colorize('$', Fore.GREEN)} "
                f"{flag.ljust(max_len)} : {color_ansi}{value_str}\033[0m"
            )

    print()
    print("‾" * total_width)


def banner_info():
    if output_print:
        try:
            with open("./src/output/version.txt", "r") as f:
                version = f.read().strip() or "?.?.?b?-vwvf"
        except FileNotFoundError:
            version = "?.?.?b?-vwvf"

        if version == "?.?.?b?-vwvf":
            print(f"{colorize("There's probably something wrong with this version.", "\033[41m")}")

        print_line(
            colorize(f"pepeScraper v{version}", Fore.GREEN),
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
        f"{Fore.GREEN}{'[+] '}{Fore.RESET}"
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
                f"[{colorize(str(len(thread_links)), Fore.YELLOW)} results]"
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

        print("--" * 20 if args.download_image else "")

if __name__ == "__main__":
    banner_info()
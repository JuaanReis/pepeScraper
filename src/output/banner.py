"""
    Function for styling and information on the use of the program when running it.

    **Author:** JuaanReis       
    **Date:** 25-09-2025        
    **Last modification:** 17-11-2025         
    **E-mail:** teixeiradosreisjuan@gmail.com       
    **Version:** 1.1.5        

    **Example:**
        ```python
    from output.banner import banner_info
    
    banner_info()
        ```
"""
from src.flags import parse_args
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init
from argparse import Namespace
from src.flags import parse_args
from os import cpu_count
from config import logo, output_print
init(autoreset=True) 

nsfw_boards = [
    "h",
    "e",
    "u",
    "d",
    "s",
    "hc",
    "hm",
    "y",
    "t",
    "gif",
    "r",
    "hr",
    "i",
    "aco"
]

def banner_logo() -> str:
    if logo:
        with open("./src/output/banner.txt", "r") as f:
            logo_art = f.read()
    else:
        logo_art = ""
    return logo_art

def print_line(msg: str, size: int = 10, banner: str = ""):
    print("_" * size, msg, "_" * size)
    print(banner) 
    print()
    args = parse_args()
    args_dict = vars(args)
    max_len = max(len(flag) for flag in args_dict.keys())
    args = parse_args()
    args_dict = vars(args)
    
    max_len = max(len(flag) for flag in args_dict.keys())

    print("‾" * ((size * 2) + len(msg) + 2))
    
    for flag, value in args_dict.items():
        if value is not None:
            print(f"  $ {flag.ljust(max_len)} : {value}")

    print()
    print("‾" * ((size * 2) + len(msg) + 2))

def banner_info():
    if output_print:
        with open("./src/output/version.txt", "r") as f:
            version = f.read()
        print_line(f"pepeScreper {version}", 35, banner_logo())

def process_thread(board, thread, args):
    url = thread.get("url", "unknown")

    if board in nsfw_boards and not args.nsfw_title:
        title = f"{Fore.RED}[Title blocked on NSFW boards]{Style.RESET_ALL}"
    else:
        title = thread.get("title", "Title not found")

    return f"{Fore.GREEN}[+] {Style.RESET_ALL}{Fore.YELLOW}{url}{Style.RESET_ALL} -> {Fore.MAGENTA}{title}{Style.RESET_ALL}"

def display_links(links: dict, args: Namespace):
    args = parse_args()
    max_threads = min(args.threads, cpu_count() * 5)
    for board, thread_links in links.items():
        print()
        if output_print:
            print(f"{Fore.CYAN}[Board {board}]{Style.RESET_ALL} → {len(thread_links)} results")
            print("-" * (8 + len(board)))

        if not thread_links:
            print(f"{Fore.RED}[-] Link not found{Style.RESET_ALL}")
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
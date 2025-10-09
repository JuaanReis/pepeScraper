"""
    Function for styling and information on the use of the program when running it.

    **Author:** JuaanReis       
    **Date:** 25-09-2025        
    **Last modification:** 08-10-2025       
    **E-mail:** teixeiradosreisjuan@gmail.com       
    **Version:** 1.1.3b2        

    **Example:**
        ```python
    from output.banner import banner_info
    
    banner_info()
        ```
"""
from src.flags import parse_args
from colorama import Fore, Style, init
init(autoreset=True) 

with open("./src/output/version.txt", "r") as f:
    version = f.read()

def banner_logo():
    with open("./src/output/banner.txt", "r") as f:
        logo = f.read()
    return logo

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
    print_line(f"pepeScreper {version}", 35, banner_logo())

def display_links(links: dict):

    for board, thread_links in links.items():

        print(f"{Fore.CYAN}[Board {board}]{Style.RESET_ALL}")
        print("-" * (8 + len(board)))

        if thread_links:
            for i, link in enumerate(thread_links, 1):
                print(f"{Fore.GREEN}[+] {Style.RESET_ALL}{link}")
        else:
            print(f"{Fore.RED}[-] Link not found{Style.RESET_ALL}")
        
        print()

if __name__ == "__main__":
    banner_info()
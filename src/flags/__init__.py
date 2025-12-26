"""
    Function that returns the flags for user-program communication.

    **Author:** JuaanReis               
    **Date:** 24-09-2025        
    **Last modification:** 25-12-2025         
    **E-mail:** teixeiradosreisjuan@gmail.com       
    **Version**  1.1.5rc2    

    **Example:**
        ```python
    from flags import parse_args

    args = parse_args()
    key = args.key
    print(key)
        ```
"""

import argparse, sys
from argparse import Namespace
from datetime import datetime
from src.output.helper import show_help

def parse_date(d: str):
    if not d:
        return None
    try:
        return datetime.strptime(d, "%Y/%m/%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format: {d}. Expected YYYY/MM/DD")

def parse_args() -> Namespace | None:
    parser = argparse.ArgumentParser(description="A tool that returns you 4chan boards", add_help=False)

    if "-h" in sys.argv or "--help" in sys.argv:
        show_help()
        sys.exit(0)
        
    parser.add_argument("--thread", "-t", type=int)
    parser.add_argument("--key", "-k", nargs="+")
    parser.add_argument("--date", type=parse_date)
    parser.add_argument("--before", type=parse_date)
    parser.add_argument("--after", type=parse_date)
    parser.add_argument("--min-replies", "-mnr", type=int)
    parser.add_argument("--max-replies", "-mxr", type=int)
    parser.add_argument("--board", "-b", nargs="+")
    parser.add_argument("--threads", "-T", type=int, default=35)
    parser.add_argument("--op-only", "-op", action="store_true")
    parser.add_argument("--no-op", "-nop", action="store_true")
    parser.add_argument("--nsfw", "-n", action="store_true", default=False)
    parser.add_argument("--output", "-o", type=str)
    parser.add_argument("--nsfw-title", "-nt", action="store_true")
    parser.add_argument("--download_image", "-di", default="")
    parser.add_argument("--proxy", "-p", type=str, default="")
    parser.add_argument("--log", action="store_true", default=False)
    parser.add_argument("--all-boards", "-ab", action="store_true", default=False)
    args = parser.parse_args()

    if not args.key or not args.board:
        if not args.all_boards:
            print("[INPUT ERROR] You must specify the keyword (-k) and the board (-b) specified.")
            sys.exit(0)

    return args
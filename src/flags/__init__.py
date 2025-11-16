"""
    Function that returns the flags for user-program communication.

    **Author:** JuaanReis               
    **Date:** 24-09-2025        
    **Last modification:** 15-11-2025       
    **E-mail:** teixeiradosreisjuan@gmail.com       
    **Version** 1.1.4rc1     

    **Example:**
        ```python
    from flags import parse_args

    args = parse_args()
    key = args.key
    print(key)
        ```
"""

import argparse
from argparse import Namespace

def parse_args() -> Namespace | None:
    try:
        parse = argparse.ArgumentParser(description="A tool that returns you 4chan boards")
        parse.add_argument("--thread", "-t", type=int, help="-t <nnnnnn>")
        parse.add_argument("--key", "-k", nargs="+", type=str, help="--key <keyword>", required=True)
        parse.add_argument("--exclude", type=str, help="--exclude <key1, key2, key3>")
        parse.add_argument("--date", type=str, help="--date <YYYY/MM/DD>")
        parse.add_argument("--before", type=str, help="--before <YYYY/MM/DD>")
        parse.add_argument("--after", type=str, help="--after <YYYY/MM/DD>")
        parse.add_argument("--min-replies", "-mnr", type=int, help="--min-replies <n>")
        parse.add_argument("--max-replies", "-mxr", type=int, help="--max-replies <n>")
        parse.add_argument("--board", "-b", nargs="+", type=str, help="--board <board_name>", required=True)
        parse.add_argument("--threads", "-T", type=int, default=30, help="-T <n>")
        parse.add_argument("--op-only", "-op", action="store_true", help="Correspond only with the op post -op <Literal [False]>")
        parse.add_argument("--no-op", "-nop", action="store_true", help="Ignore OP -nop <Literal [False]>")
        parse.add_argument("--nsfw", "-n", action="store_true", help="Enable a nsfw contents -no-nsfw <Literal [False]>", default=False)
        parse.add_argument("--output", "-o", type=str, help="Save results in file.txt <n/n/n.txt>")
        parse.add_argument("--nsfw-title", "-nt", action="store_true", help="Enable a title nsfw <Literal [False]>")
        args = parse.parse_args()
        return args
    except argparse.ArgumentTypeError:
        return None
"""
    Function that returns the flags for user-program communication.

    Author: JuaanReis
    Date: 24-09-2025
    Last modification: -
    E-mail: teixeiradosreisjuan@gmail.com
    Version: 0.0.1

    Example:
        from flags import parse_args

        args = parse_args
        key = args.key
        print(key)
"""

import argparse
from argparse import Namespace

def parse_args() -> Namespace | None:
    try:
        parse = argparse.ArgumentParser(description="A tool that returns you 4chan boards")
        parse.add_argument("--key", "-k", type=str, help="--key <keyword>")
        parse.add_argument("--exclude", type=str, help="--exclude <key1, key2, key3>")
        parse.add_argument("--date", type="str", help="--date <YYYY/MM/DD>")
        parse.add_argument("--before", type=str, help="--before <YYYY/MM/DD>")
        parse.add_argument("--after", type=str, help="--after <YYYY/MM/DD>")
        parse.add_argument("--last", type=int, help="--last <n>")
        parse.add_argument("--min-replies", "-mnr", type=int, help="--min-replies <n>")
        parse.add_argument("--max-replies", "-mxr", type=int, help="--max-replies <n>")
        args = parse_args()
        return args
    except argparse.ArgumentTypeError:
        return None
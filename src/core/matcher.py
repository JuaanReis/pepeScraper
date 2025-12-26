"""
    Function that joins the flag values for an accurate search.

    **Author:** JuaanReis  
    **Date:** 25-09-2025  
    **Last modification:** 25-12-2025    
    **E-mail:** teixeiradosreisjuan@gmail.com  
    **Version:**  1.1.5rc2 

    **Example:**
        ```python
    from src.core.matcher import thread_matches
    if thread_matches(thread_info, args):
        print("pass")
    else:
        print("doesn't pass")
        ```
"""

import re
from datetime import datetime
import json

with open("./src/core/no_nsfw.json", "r") as f:
    NSFW_KEYWORDS = tuple(k.lower() for k in json.load(f))

NSFW_BOARDS = {"a","h","e","u","d","s","hc","hm","y","t","gif","r","hr","wg"}

def check_date(timestamp, args):
    if not timestamp:
        return True

    post_date = datetime.utcfromtimestamp(timestamp).date()

    if args.date and post_date != args.date:
        return False
    if args.before and post_date >= args.before:
        return False
    if args.after and post_date <= args.after:
        return False

    return True

def check_replies(replies, args):
    if args.min_replies and replies < args.min_replies:
        return False
    if args.max_replies and replies > args.max_replies:
        return False
    return True

def select_posts(posts, args):
    if args.op_only:
        return posts[:1]
    if args.no_op:
        return posts[1:]
    return posts

def check_nsfw(posts, allow_nsfw):
    if allow_nsfw:
        return True

    for p in posts:
        com = (p.get("com") or "").lower()

        if p.get("rating", "").lower() == "nsfw":
            return False

        if any(w in com for w in NSFW_KEYWORDS):
            return False

    return True

def contains_keywords(posts, keys):
    if not keys:
        return True

    for p in posts:
        text = (p.get("com") or "").lower()
        if any(k in text for k in keys):
            return True
    return False

def contains_excluded(posts, ex_re):
    if not ex_re:
        return False
    for p in posts:
        com = (p.get("com") or "")
        if com and ex_re.search(com.lower()):
            return True
    return False

def thread_matches(thread_info, args):
    if not thread_info:
        return False

    posts = thread_info.get("posts")
    if not posts:
        return False

    board = thread_info.get("board", "").lower()

    if not args.nsfw and board in NSFW_BOARDS:
        return False

    op = posts[0]

    if not check_date(op.get("time"), args):
        return False

    if not check_replies(op.get("replies", 0), args):
        return False

    posts = select_posts(posts, args)

    allow_nsfw = args.nsfw
    keywords = args.key

    for p in posts:
        com = p.get("com")
        text = com.casefold() if com else ""

        if not allow_nsfw:
            if p.get("rating", "").lower() == "nsfw":
                return False
            if text and any(w in text for w in NSFW_KEYWORDS):
                return False
            
        if keywords and any(k in text for k in keywords):
            return True

    if keywords:
        return False

    return True

"""
    Function that joins the flag values for an accurate search.

    **Author:** JuaanReis  
    **Date:** 25-09-2025  
    **Last modification:** 25-12-2025    
    **E-mail:** teixeiradosreisjuan@gmail.com  
    **Version:**  1.1.5rc2 

    **Example:**
        ```python
    from core.matcher import thread_matches
    if thread_matches(thread_info, args):
        print("pass")
    else:
        print("doesn't pass")
        ```
"""

import re
from datetime import datetime
import json

with open("./data/no_nsfw.json", "r") as f:
    NSFW_KEYWORDS = tuple(k.lower() for k in json.load(f))

NSFW_REGEX = re.compile(
    r"(?<!\w)(" + "|".join(map(re.escape, NSFW_KEYWORDS)) + r")(?!\w)",
    re.IGNORECASE
)

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

def image_name_matches(posts, keywords):
    if not keywords:
        return True

    for p in posts:
        filename = (p.get("filename") or "").lower()
        ext = (p.get("ext") or "").lower()

        if not filename:
            continue  

        full_name = filename + ext

        if any(k.lower() in full_name for k in keywords):
            return True

    return False

def title_matches(op, keywords):
    if not keywords:
        return True

    title = (op.get("sub") or "")
    if not title:
        return False

    pattern = r"(?<!\w)(" + "|".join(map(re.escape, keywords)) + r")(?!\w)"
    return re.search(pattern, title, re.IGNORECASE) is not None

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
        text = (p.get("com") or "").casefold()

        if p.get("rating", "").lower() == "nsfw":
            return False

        if text and NSFW_REGEX.search(text):
            return False

    return True

def keyword_regex(keywords):
    return re.compile(
        r"(?<!\w)(" + "|".join(map(re.escape, keywords)) + r")(?!\w)",
        re.IGNORECASE
    )

def contains_keywords(posts, keys):
    if not keys:
        return True

    rgx = keyword_regex(keys)

    for p in posts:
        text = (p.get("com") or "")
        if rgx.search(text):
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
    allow_nsfw = args.nsfw
    keywords = args.key

    if not thread_info:
        return False

    posts = thread_info.get("posts")
    if not posts:
        return False

    board = thread_info.get("board", "").lower()

    if not args.nsfw and board in NSFW_BOARDS:
        return False

    op = posts[0]

    if args.title and not title_matches(op, keywords):
        return False
    
    if args.image and not image_name_matches(posts, keywords):
        return False

    if not check_date(op.get("time"), args):
        return False

    if not check_replies(op.get("replies", 0), args):
        return False

    posts = select_posts(posts, args)

    for p in posts:
        com = p.get("com")
        text = com.casefold() if com else ""

        if not allow_nsfw:
            if p.get("rating", "").lower() == "nsfw":
                return False
            if text and any(w in text for w in NSFW_KEYWORDS):
                return False

        if keywords:
            rgx = keyword_regex(keywords)
            if rgx.search(text):
                return True

    if keywords:
        return False

    return True

"""
    Function that joins the flag values for an accurate search.

    **Author:** JuaanReis  
    **Date:** 25-09-2025  
    **Last modification:** 17-11-2025    
    **E-mail:** teixeiradosreisjuan@gmail.com  
    **Version:** 1.1.5  

    **Example:**
        ```python
    from src.core.matcher import thread_matches
    if thread_matches(thread_info, args):
        print("pass")
    else:
        print("doesn't pass")
        ```
"""

from datetime import datetime
import re, json

with open(r"src\core\no_nsfw.json", "r") as f:
    NSFW_KEYWORDS = tuple(k.lower() for k in json.load(f))  

NSFW_BOARDS = {"a","h","e","u","d","s","hc","hm","y","t","gif","r","hr","wg"}

def build_exclude_regex(excludes_str: str):
    
    parts = [
        re.escape(ex.strip().lower())
        for ex in re.split(r"[,\s]+", excludes_str)
        if ex.strip()
    ]

    if not parts:
        return None
    
    pattern = r"(?<!\w)(?:%s)(?!\w)" % "|".join(parts)
    return re.compile(pattern)

def thread_matches(thread_info, args):
    if not thread_info:
        return False

    posts = thread_info.get("posts")
    if not posts:
        return False

    allow_nsfw = getattr(args, "nsfw", True)

    if not allow_nsfw and thread_info.get("board", "").lower() in NSFW_BOARDS:
        return False

    timestamp = posts[0].get("time")
    if timestamp:
        post_date = datetime.utcfromtimestamp(timestamp).date()

        if args.date and post_date != datetime.strptime(args.date, "%Y/%m/%d").date():
            return False

        if args.before and post_date >= datetime.strptime(args.before, "%Y/%m/%d").date():
            return False

        if args.after and post_date <= datetime.strptime(args.after, "%Y/%m/%d").date():
            return False

    replies = posts[0].get("replies", 0)
    if args.min_replies and replies < args.min_replies:
        return False
    if args.max_replies and replies > args.max_replies:
        return False

    if getattr(args, "op_only", False):
        posts_to_check = posts[:1]
    elif getattr(args, "no_op", False):
        posts_to_check = posts[1:]
    else:
        posts_to_check = posts

    if not allow_nsfw:
        for post in posts_to_check:
            com = post.get("com")
            if not com:
                continue
            com = com.lower()

            if post.get("rating", "").lower() == "nsfw":
                return False

            if any(w in com for w in NSFW_KEYWORDS):
                return False
            
    if args.key:
        keys_lower = tuple(k.lower() for k in args.key)

        if not any(
            any(k in (p.get("com", "").lower()) for k in keys_lower)
            for p in posts_to_check
        ):
            return False

    if args.exclude:
        ex_re = build_exclude_regex(args.exclude)
        if ex_re:
            for p in posts_to_check:
                com = p.get("com", "")
                if com and ex_re.search(com.lower()):
                    return False

    return True
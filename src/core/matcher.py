"""
    Function that joins the flag values for an accurate search.

    **Author:** JuaanReis  
    **Date:** 25-09-2025  
    **Last modification:** 08-10-2025  
    **E-mail:** teixeiradosreisjuan@gmail.com  
    **Version:** 1.1.3b2  

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

def keywords_no_nsfw() -> list:
    with open(r"src\core\no_nfsw.json", "r") as f:
        nfsw_keywords = json.load(f)
    return nfsw_keywords

nfsw_keywords = keywords_no_nsfw()

def thread_matches(thread_info, args):
    if not thread_info:
        return False

    posts = thread_info.get("posts", [])
    if not posts:
        return False

    timestamp = posts[0].get("time")
    if timestamp:
        post_date = datetime.utcfromtimestamp(timestamp)
        if args.date:
            filter_date = datetime.strptime(args.date, "%Y/%m/%d")
            if post_date.date() != filter_date.date():
                return False
        if args.before:
            before_date = datetime.strptime(args.before, "%Y/%m/%d")
            if post_date.date() >= before_date.date():
                return False
        if args.after:
            after_date = datetime.strptime(args.after, "%Y/%m/%d")
            if post_date.date() <= after_date.date():
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

    if getattr(args, "no_nsfw", False):
        for post in posts_to_check:
            if post.get("rating", "").lower() == "nsfw":
                return False

            content_lower = post.get("com", "").lower()
            if any(word in content_lower for word in nfsw_keywords):
                return False

    content = " ".join([post.get("com", "") for post in posts_to_check])
    if args.key:
        content_lower = content.lower()
        if args.key and not any(word.lower() in content_lower for word in args.key):
            return False
    if args.exclude:
        for ex in re.split(r"[,\s]+", args.exclude.strip()):
            if ex.lower().strip() in content:
                return False

    return True

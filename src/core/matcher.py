"""
    Function that joins the flag values for an accurate search.

    **Author:** JuaanReis  
    **Date:** 25-09-2025  
    **Last modification:** 15-11-2025  
    **E-mail:** teixeiradosreisjuan@gmail.com  
    **Version:** 1.1.4rc1  

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

def extract_content(posts_to_check):
    for p in posts_to_check:
        com = p.get("com", "")
        if com:
            yield com.lower()

def keywords_no_nsfw() -> list:
    with open(r"src\core\no_nsfw.json", "r") as f:
        return json.load(f)

nsfw_keywords = keywords_no_nsfw()

def thread_matches(thread_info, args):
    if not thread_info:
        return False

    posts = thread_info.get("posts", [])
    if not posts:
        return False
    
    allow_nsfw = getattr(args, "nsfw", True)

    board = thread_info.get("board", "").lower()
    nsfw_boards = {"a","h","e","u","d","s","hc","hm","y","t","gif","r","hr","wg"}

    if not allow_nsfw:
        if board in nsfw_boards:
            return False

    timestamp = posts[0].get("time")
    if timestamp:
        post_date = datetime.utcfromtimestamp(timestamp)

        if args.date:
            if post_date.date() != datetime.strptime(args.date, "%Y/%m/%d").date():
                return False

        if args.before:
            if post_date.date() >= datetime.strptime(args.before, "%Y/%m/%d").date():
                return False

        if args.after:
            if post_date.date() <= datetime.strptime(args.after, "%Y/%m/%d").date():
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
            if post.get("rating", "").lower() == "nsfw":
                return False

            content_lower = post.get("com", "").lower()
            if any(word in content_lower for word in nsfw_keywords):
                return False
            
    if args.key:
        keys_lower = [k.lower() for k in args.key]
        found_key = False

        for com in extract_content(posts_to_check):
            if any(k in com for k in keys_lower):
                found_key = True
                break

        if not found_key:
            return False

    if args.exclude:
        excludes = [
            ex.strip().lower()
            for ex in re.split(r"[,\s]+", args.exclude)
            if ex.strip()
        ]

        for post in posts_to_check:
            content_lower = post.get("com", "").lower()
            for ex in excludes:
                if re.search(rf"(?<!\w){re.escape(ex)}(?!\w)", content_lower):
                    return False


    return True
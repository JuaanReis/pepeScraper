from src.output.banner import banner_info, display_links
from src.core.search_posts import search_threads, build_thread_links, save_log
from src.core.output import download_output
from src.flags import parse_args
from config import color_ansi 
from time import time

def main():
    start_run = time()
    args = parse_args()
    banner_info()
    start = time()
    results = search_threads(args)
    end = time()
    links = build_thread_links(results)
    save_log(links, args)
    display_links(links, args)
    download_output(args, links, results)
    end_run = time()
    print("--" * 20)
    print(f"Requests made in {color_ansi}{end - start:.2f}\033[0ms")
    print(f"Task completed in {color_ansi}{end_run - start_run:.2f}\033[0ms")
            
if __name__ == "__main__":
    main()
from src.output.banner import banner_info, display_links
from src.core.search_posts import search_threads, build_thread_links, save_links
from src.flags import parse_args
import time

def main():
    args = parse_args()
    banner_info()
    start = time.time()
    results = search_threads(args)
    end = time.time()
    links = build_thread_links(results)
    display_links(links, args)
    if args.output != "":
        save_links(links, args.output)
    else:
        print()

    print(f"Task completed in {end - start:.2f}s")
            
if __name__ == "__main__":
    main()
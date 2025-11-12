from src.output.banner import banner_info, display_links
from src.core.search_posts import search_threads, build_thread_links, save_links
from src.flags import parse_args

def main():
    args = parse_args()
    banner_info()
    results = search_threads(args)
    links = build_thread_links(results)
    display_links(links)
    if args.save_result != "":
        save_links(links, args.save_result)
    else:
        print()
            
if __name__ == "__main__":
    main()
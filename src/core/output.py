from argparse import Namespace
from src.core.download_img import download_thread_images
from src.core.search_posts import save_links

def download_output(args: Namespace, links: dict, results: dict):
    if args.output is not None:
        save_links(links, args.output)
    if args.download_image: 
        print("--" * 20)
        i = 0
        for board, thread_list in results.items():
            for thread_no in thread_list:
                i += 1
                download_thread_images(board, i, thread_no, args.download_image)
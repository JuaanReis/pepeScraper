"""
    Function that downloads the output and images from the threads.

    **Author:** JuaanReis  
    **Date:** 07-12-2025  
    **Last modification:** -    
    **E-mail:** teixeiradosreisjuan@gmail.com  
    **Version:** 1.1.5rc2 

    **Example:**
        ```python
    from src.core.output import download_output

    download_output(args, links, results)
        ```
"""

from argparse import Namespace
from src.core.download_img import download_thread_images
from src.core.search_posts import save_links
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import config

def download_output(args: Namespace, links: dict, results: dict):
    if args.output:
        save_links(links, args.output)

    if not args.download_image:
        return

    tasks = []
    total_threads = sum(len(tlist) for tlist in results.values())

    with ThreadPoolExecutor(max_workers=args.threads or 10) as executor:
        for board, thread_list in results.items():
            for thread_no in thread_list:
                tasks.append(
                    executor.submit(
                        download_thread_images,
                        board,
                        thread_no,
                        args.download_image
                    )
                )

        with tqdm(
            total=total_threads,
            desc="Downloading threads",
            bar_format=config.color_ansi + "{l_bar}{bar}{r_bar}" + "\033[0m",
            ncols=100
        ) as pbar:

            for future in as_completed(tasks):
                try:
                    future.result()
                except Exception as e:
                    if config.debug:
                        print(f"[ERROR DOWNLOAD OUTPUT] {e}")
                finally:
                    pbar.update(1)

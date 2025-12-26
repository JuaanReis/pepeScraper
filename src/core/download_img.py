"""
    Download the images from each post.

    **Author:** JuaanReis  
    **Date:** 2-12-2025  
    **Last modification:** 25-12-2025
    **E-mail:** teixeiradosreisjuan@gmail.com  
    **Version:** 1.1.5

    **Example:**
        ```python
    from src.core.download_img import download_thread_images
    download_thread_images("o", 28745723, "downloads")
        ```
"""
import os
from src.network.get_all_boards import get_response

def download_thread_images(board: str, thread_no: int, output_dir="images"):
    api_url = f"https://a.4cdn.org/{board}/thread/{thread_no}.json"

    r = get_response(api_url)
    if r.status_code != 200:
        return False

    data = r.json()

    folder = os.path.join(output_dir, f"{board}_{thread_no}")
    os.makedirs(folder, exist_ok=True)

    for post in data["posts"]:
        if "tim" in post:
            tim = post["tim"]
            ext = post["ext"]
            img_url = f"https://i.4cdn.org/{board}/{tim}{ext}"

            img_path = os.path.join(folder, f"{tim}{ext}")

            try:
                img_resp = get_response(img_url)
                if img_resp.status_code == 200:
                    with open(img_path, "wb") as f:
                        f.write(img_resp.content)
            except:
                pass

    return True
"""
    Functions that search and return all 4chan boards, ensuring the project
    does not use deprecated boards and none are left out.

    **Author:** JuaanReis       
    **Date:** 28-08-2025        
    **Last modification:** 17-11-2025         
    **E-mail:** teixeiradosreisjuan@gmail.com           
    **Version:** 1.1.5        

    **Example:**
        ```python
    from get_all_boards import get_boards_api

    boards = get_boards_api()

    for board in boards:
        print(board)
        ```
"""

import httpx
import orjson as json
import config
import time

client = config.client

def get_response(url: str, retries: int = 3, delay: float = 0.5) -> httpx.Response | None:
    for attempt in range(retries):
        try:
            response = client.get(url)
            response.raise_for_status()
            return response

        except httpx.HTTPStatusError as e:
            status = e.response.status_code
            if status == 429:
                retry_after = int(e.response.headers.get("Retry-After", 1))
                if config.debug:
                    print(f"[429 RATE LIMIT] {url} -> retry in {retry_after}s")
                time.sleep(retry_after)
                continue

            if config.debug:
                print(f"[HTTP STATUS ERROR] {url} -> {status}")
            return None

        except httpx.ConnectError as e:
            msg = str(e)

            if "10035" in msg:
                if config.debug:
                    print(f"[SOCKET BUSY] {url} -> retry {attempt+1}/{retries}")
                time.sleep(delay * (1 + attempt * 0.75))
                continue

            if "Name or service not known" in msg:
                if config.debug:
                    print(f"[DNS FAIL] {url}")
                return None

            if config.debug:
                print(f"[CONNECT ERROR] {url} -> {e}")
            time.sleep(delay * (1 + attempt * 0.75))
            continue

        except httpx.RequestError as e:
            if config.debug:
                print(f"[REQUEST ERROR] {url} -> {e}")
            time.sleep(delay * (1 + attempt * 0.75))
            continue

        except Exception as e:
            if config.debug:
                print(f"[UNEXPECTED ERROR] {url} -> {e}")
            time.sleep(delay * (1 + attempt * 0.75))
            continue

    try:
        return client.get(url, timeout=10)
    except:
        pass

    if config.debug:
        print(f"[FAILED AFTER RETRIES] {url}")
    return None


def get_boards_api() -> dict:
    start = time.time()
    boards = get_response("https://a.4cdn.org/boards.json")
    if not boards:
        print("ERROR: could not access the api.")
        if config.debug and boards is not None:
            print(f"[API STATUS] {boards.status_code}")
        return

    data = json.dumps(
        boards.json(),
        option=json.OPT_INDENT_2 
    )

    with open("./src/data/boards.json", "wb") as f:
        f.write(data)

    end = time.time()

    print(f"save in {end - start:.2f}s")

    return boards.json()

if __name__ == "__main__":
    get_boards_api()
import config
from argparse import Namespace

def save_log(links: dict, args: Namespace):
    if args.log:
        pathlog = args.log
    else:
        import os
        os.makedirs("./src/data/logs", exist_ok=True)
        pathlog = "./src/data/logs"
    if config.logs or args.log:
        from datetime import datetime
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"log_{timestamp}.log"
            filepath = os.path.join(pathlog, filename)

            with open(filepath, "w", encoding="utf-8") as f:

                f.write("==============================================\n")
                f.write("                PEPESCRAPER LOG               \n")
                f.write("==============================================\n")

                now = datetime.now()
                f.write(f"DATE: {now.strftime('%Y/%m/%d')}\n")
                f.write(f"HOUR: {now.strftime('%H:%M:%S')}\n")

                f.write("\n[ARGS]\n")
                f.write("------------------------------------------\n")
                for key, value in vars(args).items():
                    f.write(f"{key}: {value}\n")

                f.write("\n")

                for board, link_list in links.items():

                    f.write(f"\n[Board {board}] ({len(link_list)} threads)\n")
                    f.write("------------------------------------------\n")

                    for idx, link_data in enumerate(link_list, start=1):
                        url = link_data.get("url", "N/A")
                        title = link_data.get("title", "[No title]")
                        comment = link_data.get("comment", "")

                        f.write(f"#{idx}\n")
                        f.write(f"URL: {url}\n")
                        f.write(f"TITLE: {title}\n")
                        f.write(f"COMMENT:\n{comment}\n")
                        f.write("------------------------------------------\n")

            if config.debug:
                print(f"[LOG SALVO]: {filepath}")

        except Exception as e:
            if config.debug:
                print(f"[ERROR SAVE LOG]: {e}")

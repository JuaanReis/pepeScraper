def show_help():
    print(r"""
___________________________________ pepeScraper ___________________________________

USAGE:
    py main.py -k <keywords> -b <boards> [options]

DESCRIPTION:
    A fast multithreaded 4chan scraper with keyword matching, 
    date filtering, NSFW control, thread scanning and image downloading.

REQUIRED:
    -k, --key <word1 word2 ...>
        Keywords to search for. Case-insensitive.
    
    -b, --board <board1 board2 ...>
        Boards to scrape. Example: -b o fit g

NETWORK:
    -proxy, -p <w>
        Activate the proxy.          

FILTERS:
    --date <YYYY/MM/DD>
        Only match posts on this exact date.

    --before <YYYY/MM/DD>
        Only match posts created *before* this date.

    --after <YYYY/MM/DD>
        Only match posts created *after* this date.

    -mnr, --min-replies <n>
        Only match threads with at least N replies.

    -mxr, --max-replies <n>
        Only match threads with at most N replies.

THREAD BEHAVIOR:
    -T, --threads <n>
        Number of worker threads. Default = 35.

    -op, --op-only
        Only match the OP post (ignore replies).

    -nop, --no-op
        Ignore the OP post (only scan replies).

NSFW CONTROL:
    -n, --nsfw
        Enable NSFW content scanning.

    -nt, --nsfw-title
        Allow NSFW content in titles.

OUTPUT:
    -o, --output <file>
        Save matched results to a file.

    -di, --download_image <directory>
        Download all images from matched threads.
          
    --log
        Activate the log that is saved in "./src/data/logs"

MISC:
    -t, --thread <id>
        Scan only a single thread ID.

    -h, --help
        Show this help message.
          
    --all-boards, -ab
        Shows all 4chan boards with their respective descriptive titles.

EXAMPLES:
    py main.py -k car -b o
    py main.py -k supra skyline -b o fit -T 80
    py main.py -k cat -b a -after 2024/01/01 -mnr 10
____________________________________________________________________________________
""")
    exit(0)


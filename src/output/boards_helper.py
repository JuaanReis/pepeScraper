from src.utils.color import colorize

def board_help(boards: dict):
    BOARD_WIDTH = 5
    TITLE_WIDTH = 30
    STATUS_WIDTH = 10

    print(colorize(
        f"{'BOARD':<{BOARD_WIDTH}} | {'TITLE':<{TITLE_WIDTH}} | {'STATUS':<{STATUS_WIDTH}}",
        "\033[36m"
    ))

    print(colorize(
        f"{'-'*BOARD_WIDTH}-+-{'-'*TITLE_WIDTH}-+-{'-'*STATUS_WIDTH}",
        "\033[34m"
    ))

    for b in boards["boards"]:
        board_code = f"{b['board']:<{BOARD_WIDTH}}"
        title_base = f"{b['title']:<{TITLE_WIDTH}}"

        if b.get("is_archived"):
            board = board_code
            status = colorize(f"{'ARCHIVED':<{STATUS_WIDTH}}", "\033[31m")
        else:
            board = colorize(board_code, "\033[32m")
            status = colorize(f"{'ACTIVE':<{STATUS_WIDTH}}", "\033[32m")

        print(f"{board} | {title_base} | {status}")

def print_boards():
    from src.flags import parse_args
    from json import load
    from sys import exit
    args = parse_args()
    with open("./src/data/boards.json", "r") as f:
        b_file = load(f)
        if args.all_boards:
            board_help(b_file)
            exit(0)
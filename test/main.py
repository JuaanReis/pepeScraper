from src.network.get_all_boards import get_boards_api

def main():
    boards = get_boards_api()
    print(boards)

if __name__ == "__main__":
    main()
from chezz.game import State


def main() -> None:
    game = State()

    while True:
        print(game)
        cmd = input("> ")

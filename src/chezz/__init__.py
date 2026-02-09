from chezz.game import State
from chezz.geo.v2 import V2


def main() -> None:
    game = State()

    while True:
        print(game)
        cmd = input("> ")
        args = cmd.split()
        if not args:
            continue

        match args[0]:
            case "get":
                if len(args) == 1:
                    continue
                coord = V2.from_notation(args[1])
                game.selected = coord
                idx = coord.into_idx()
                print(game.get_positions()[0][idx])
            case "go":
                if len(args) != 3:
                    continue
                c1 = V2.from_notation(args[1])
                c2 = V2.from_notation(args[2])
                diff = c2 - c1
                print(f"Try moving {game.get_positions()[0][c1.into_idx()]} by {diff}")
            case "exit":
                return

from pathlib import Path


def parse_maze(path: Path) -> list[list[str]]:
    with open(path) as f:
        lines = list(map(list, f.read().splitlines()))

    return lines


def main() -> None:
    maze = parse_maze(Path("data/sample16.txt"))


if __name__ == "__main__":
    main()

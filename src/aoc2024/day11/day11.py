from pathlib import Path


def read_input(path: Path) -> list[int]:
    with open(path) as f:
        stones = map(int, f.read().strip().split())
    return list(stones)


def evolve_stone(stone: int) -> list[int]:
    match stone:
        case 0:
            return [1]
        case stone if (stone_digit_count := len(stone_string := str(stone))) % 2 == 0:
            return [int(stone_string[: (stone_mid := stone_digit_count // 2)]), int(stone_string[stone_mid:])]
        case _:
            return [2024 * stone]


def repeated_apply(stones: list[int], apply_count: int, memo_dict: dict[tuple[int, int], int]) -> int:
    if apply_count == 0:
        return len(stones)
    result = 0
    for s in stones:
        if (s, apply_count) in memo_dict:
            result += memo_dict[(s, apply_count)]
        else:
            sum_for_s = repeated_apply(evolve_stone(s), apply_count - 1, memo_dict)
            memo_dict[(s, apply_count)] = sum_for_s
            result += sum_for_s
    return result


def main() -> None:
    stones = read_input(Path("data/input11.txt"))
    memo_dict: dict[tuple[int, int], int] = {}
    print(repeated_apply(stones, 25, memo_dict))
    print(repeated_apply(stones, 75, memo_dict))


if __name__ == "__main__":
    main()

from pathlib import Path
from typing import Callable, Iterable


def parse_input(path: Path) -> tuple[list[str], list[str]]:
    with open(path) as f:
        blocks = f.read().split("\n\n")
    available = list(map(lambda s: s.strip(), blocks[0].split(",")))
    desired = blocks[1].splitlines()
    return available, desired


def try_to_match(
    desired: str, available: list[str], memo_dict: dict[str, int], accumulator: Callable[[Iterable[int]], int]
) -> int:
    if desired in memo_dict:
        return memo_dict[desired]
    if desired == "":
        return 1
    candidates = [x for x in available if x == desired[: len(x)]]
    if not candidates:
        return 0
    memo_dict[desired] = accumulator(
        try_to_match(desired[len(c) :], available, memo_dict, accumulator) for c in candidates
    )
    return memo_dict[desired]


def main() -> None:
    available, desired = parse_input(Path("data/input19.txt"))
    can_match_dict: dict[str, int] = {}
    print(sum(try_to_match(d, available, can_match_dict, lambda x: int(any(x))) for d in desired))
    combo_count_dict: dict[str, int] = {}
    print(sum(try_to_match(d, available, combo_count_dict, sum) for d in desired))

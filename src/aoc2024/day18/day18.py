import functools
import itertools
import math
from collections import OrderedDict
from copy import deepcopy
from pathlib import Path

from graph_utils import dijkstra

type Coord = tuple[int, int]


def get_bytes(path: Path) -> list[Coord]:
    with open(path) as f:
        lines = f.read().splitlines()
    return list(map(lambda x: (int((coords := x.strip("()").split(","))[1]), int(coords[0])), lines))


def get_neighbours(
    current_distance: float,
    current_position: Coord,
    unvisted_set: set[Coord],
    placed_bytes: set[Coord],
    max_row: int,
    max_col: int,
) -> dict[Coord, float]:
    current_row, current_col = current_position
    # can't be botherd to be smarter at this point
    possible_neighbours = [
        (current_row + 1, current_col),
        (current_row - 1, current_col),
        (current_row, current_col + 1),
        (current_row, current_col - 1),
    ]
    return {
        x: current_distance + 1
        for x in possible_neighbours
        if x not in placed_bytes and x in unvisted_set and x[0] in range(max_row + 1) and x[1] in range(max_col + 1)
    }


def can_escape(distances: OrderedDict[Coord, float], byte_list: list[Coord], max_row: int, max_col: int) -> bool:
    distances, _ = dijkstra(
        distances, functools.partial(get_neighbours, placed_bytes=set(byte_list), max_row=max_row, max_col=max_col)
    )
    return math.isfinite(distances[(max_row, max_col)])


def binary_search(
    distances: OrderedDict[Coord, float],
    upper_n_bytes: int,
    lower_n_bytes: int,
    byte_list: list[Coord],
    max_row: int,
    max_col: int,
) -> int:
    n_bytes = lower_n_bytes + (upper_n_bytes - lower_n_bytes) // 2
    can_escape_lower = can_escape(deepcopy(distances), byte_list[: (n_bytes - 1)], max_row, max_col)
    can_escape_upper = can_escape(deepcopy(distances), byte_list[:n_bytes], max_row, max_col)
    if can_escape_lower and not can_escape_upper:
        return n_bytes
    elif can_escape_lower and can_escape_upper:
        return binary_search(distances, upper_n_bytes, n_bytes - 1, byte_list, max_row, max_col)
    else:
        return binary_search(distances, n_bytes + 1, lower_n_bytes, byte_list, max_row, max_col)


def main() -> None:
    max_row = 70
    max_col = 70
    n_bytes = 1024
    byte_queue = get_bytes(Path("data/input18.txt"))

    placed_bytes = set(byte_queue[:n_bytes])
    all_coords = itertools.product(range(max_row + 1), range(max_col + 1))
    distances = OrderedDict({coord: math.inf for coord in all_coords if coord not in placed_bytes})
    distances[(0, 0)] = 0
    solved_dists, _ = dijkstra(
        deepcopy(distances),
        functools.partial(get_neighbours, placed_bytes=placed_bytes, max_row=max_row, max_col=max_col),
    )
    print(solved_dists[(70, 70)])
    first_byte_count = binary_search(distances, len(byte_queue), 1024, byte_queue, max_row, max_col)
    first_byte_coord = byte_queue[first_byte_count - 1]
    print(f"{first_byte_coord[1]},{first_byte_coord[0]}")


if __name__ == "__main__":
    main()

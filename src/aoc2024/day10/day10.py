import functools
import itertools
from copy import copy
from itertools import zip_longest
from pathlib import Path

type TrailMap = list[list[int]]
type Coord = tuple[int, int]


def parse_input(path: Path) -> TrailMap:
    with open(path) as f:
        lines = f.read().splitlines()
    trail_map = [list(map(int, list(line))) for line in lines]
    return trail_map


def get_trailheads(trail_map: TrailMap) -> list[Coord]:
    trailheads = []
    for i, row in enumerate(trail_map):
        trailheads.extend([(i, j) for j, col in enumerate(row) if col == 0])
    return trailheads


def find_valid_neighbours(
    start_point: Coord, current_height: int, trail_map: TrailMap, coord_to_neighbours: dict[Coord, list[Coord]]
) -> list[Coord]:
    """
    Get a list of neighbours that are on the map, and only increase in height by one. (And aren't start_point)
    """
    max_dim = len(trail_map)
    if start_point not in coord_to_neighbours:
        neighbours = itertools.chain.from_iterable(
            [
                zip_longest(
                    range(max(0, start_point[0] - 1), min(max_dim, start_point[0] + 2)),
                    [start_point[1]],
                    fillvalue=start_point[1],
                ),
                zip_longest(
                    [start_point[0]],
                    range(max(0, start_point[1] - 1), min(max_dim, start_point[1] + 2)),
                    fillvalue=start_point[0],
                ),
            ]
        )
        valid_neighbours = [n for n in neighbours if n != start_point and trail_map[n[0]][n[1]] == current_height + 1]
        coord_to_neighbours[start_point] = valid_neighbours
    else:
        valid_neighbours = coord_to_neighbours[start_point]
    return valid_neighbours


def depth_first(
    start_point: Coord,
    current_height: int,
    trail_map: TrailMap,
    current_path: list[Coord],
    trails_to_summit: set[tuple[Coord, ...]],
    coord_to_neighbours: dict[Coord, list[Coord]],
) -> set[Coord]:
    """
    Return coords of reachable 9s and append the path used to get here to trails_to_summit.
    We don't need no stinking memos.
    """
    if current_height == 9:
        trails_to_summit.add(tuple(current_path))
        return {start_point}
    neighbours = find_valid_neighbours(start_point, current_height, trail_map, coord_to_neighbours)
    # DO copy `current_path` before recursive call, DON'T copy `trails_to_summit` before recursive call.
    # Thought I was better than this
    # noinspection PyTypeChecker
    return functools.reduce(
        set.union,
        [
            depth_first(
                n, current_height + 1, trail_map, copy(current_path) + [n], trails_to_summit, coord_to_neighbours
            )
            for n in neighbours
        ],
        set(),
    )


def score_trailhead(head: Coord, trail_map: TrailMap, coord_to_neighbours: dict[Coord, list[Coord]]) -> tuple[int, int]:
    trails_to_summit: set[tuple[Coord, ...]] = set()
    p1_score = len(depth_first(head, 0, trail_map, [], trails_to_summit, coord_to_neighbours))
    return p1_score, len(trails_to_summit)


def solve(trail_map: TrailMap, heads: list[Coord]) -> tuple[int, int]:
    coord_to_neighbours: dict[Coord, list[Coord]] = {}
    scores = [score_trailhead(head, trail_map, coord_to_neighbours) for head in heads]
    return (summed := tuple(map(sum, zip(*scores))))[0], summed[1]


def main() -> None:
    trail_map = parse_input(Path("data/input10.txt"))
    trail_heads = get_trailheads(trail_map)
    scores = solve(trail_map, trail_heads)
    print(scores[0])
    print(scores[1])


if __name__ == "__main__":
    main()

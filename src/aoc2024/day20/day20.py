import functools
import itertools
import math
from collections import OrderedDict
from pathlib import Path

from tqdm import tqdm

from graph_utils import dijkstra, get_neighbours

type Coord = tuple[int, int]


def parse_input(path: Path) -> tuple[Coord, Coord, list[Coord], list[Coord], int, int]:
    with open(path) as f:
        lines = f.read().splitlines()
    walls = []
    track = []
    start: Coord = (0, 0)
    end: Coord = (0, 0)
    max_row = len(lines) - 1
    max_col = len(lines[0]) - 1
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            match char:
                case "#":
                    walls.append((i, j))
                case "S":
                    start = (i, j)
                case "E":
                    end = (i, j)
                case ".":
                    track.append((i, j))
    return start, end, walls, [start] + track + [end], max_row, max_col


def backtrack(
    current_point: Coord,
    node_to_previous: dict[Coord, set[Coord]],
    optimal_set: list[Coord],
    start: Coord,
) -> list[Coord]:
    """
    Iterate through the previous neighbour mapping to determine all tiles visited
    """
    optimal_set.append(current_point)
    if current_point == start:
        optimal_set.append(current_point)
        return list(reversed(optimal_set))
    return backtrack(node_to_previous[current_point].pop(), node_to_previous, optimal_set, start)


def get_distances_to_end(
    start: Coord, all_coords: list[Coord], walls: set[Coord], max_row: int, max_col: int
) -> dict[Coord, float]:
    distances = OrderedDict({coord: math.inf for coord in all_coords if coord not in walls})
    distances[start] = 0
    solved, blah = dijkstra(
        distances, functools.partial(get_neighbours, obstacles=walls, max_row=max_row, max_col=max_col)
    )
    return solved


def solve(distances: dict[Coord, float], track: list[Coord], max_cheat_time: int) -> list[float]:
    saves = []

    for a, b in tqdm(itertools.permutations(track, 2)):
        if 1 < (taxi_dist := abs(a[0] - b[0]) + abs(a[1] - b[1])) <= max_cheat_time:
            save = distances[a] - distances[b] - taxi_dist
            if save >= 100:
                saves.append(save)
    return saves


def main() -> None:
    start, end, walls, track, max_row, max_col = parse_input(Path("data/input20.txt"))
    wall_set = set(walls)
    dists_to_end = get_distances_to_end(start, track, wall_set, max_row, max_col)
    print(len(solve(dists_to_end, track, 2)))
    print(len(solve(dists_to_end, track, 20)))

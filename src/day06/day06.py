import itertools
from copy import copy, deepcopy
from dataclasses import dataclass, field
from math import sumprod
from pathlib import Path

from joblib import Parallel, delayed
from tqdm import tqdm

Coord = tuple[int, int]


class Direction:
    def __init__(self, coord: Coord) -> None:
        self._rotation_matrix = [[0, 1], [-1, 0]]
        self.coord: tuple[int, int] = coord

    def get_rotated(self) -> "Direction":
        return Direction(
            (
                int(sumprod(self._rotation_matrix[0], self.coord)),
                int(sumprod(self._rotation_matrix[1], self.coord)),
            )
        )

    @property
    def collision_indexer(self) -> int:
        return int(self.coord[0] != 0)

    @property
    def distance_indexer(self) -> int:
        return int(self.coord[0] == 0)

    @property
    def sign(self) -> int:
        return self.coord[self.distance_indexer]


@dataclass
class GuardState:
    """
    ewwww state...
    """

    position: Coord
    direction: Direction
    visited: set[Coord] = field(default_factory=set)
    objects_hit_and_direction: list[tuple[tuple[int, int], tuple[int, int]]] = field(default_factory=list)
    has_exited: bool = False
    is_looping: bool = False


def read_input(path: Path) -> tuple[list[Coord], Coord, int]:
    with open(path) as f:
        maze = f.readlines()
    obstacles: list[tuple[int, int]] = []
    start = (0, 0)
    # god I hope this is square
    side_length = len(maze)
    for i, line in enumerate(maze):
        if "#" not in line and "^" not in line:
            continue
        if "^" in line:
            start = (i, line.index("^"))

        obstacles.extend(tuple(itertools.zip_longest([i], [j for j, c in enumerate(line) if c == "#"], fillvalue=i)))
    return obstacles, start, side_length


def get_visit_set(start: Coord, finish: Coord, direction: Direction) -> set[Coord]:
    if direction.distance_indexer == 1:
        return {(start[0], i) for i in range(start[1], finish[1] + direction.sign, direction.sign)}
    else:
        return {(i, start[1]) for i in range(start[0], finish[0] + direction.sign, direction.sign)}


def update_guard_state(guard: GuardState, obstacles: list[Coord], side_length: int) -> GuardState:
    direction = guard.direction
    pos = guard.position
    obstacles = sorted(obstacles, key=lambda o: abs(o[0] - pos[0]) + abs(o[1] - pos[1]))
    obstacles_hit = list(
        itertools.dropwhile(
            lambda o: (pos[direction.collision_indexer] != o[direction.collision_indexer])
            or ((o[direction.distance_indexer] - pos[direction.distance_indexer]) * direction.sign < 0),
            obstacles,
        )
    )
    if not obstacles_hit:
        new_pos_list = [0, 0]
        new_pos_list[direction.collision_indexer] = pos[direction.collision_indexer]
        if direction.sign > 0:
            new_pos_list[direction.distance_indexer] = side_length - 1
        else:
            new_pos_list[direction.distance_indexer] = 0
        new_pos = (new_pos_list[0], new_pos_list[1])
        guard.visited.update(get_visit_set(pos, new_pos, direction))
        return GuardState(new_pos, direction.get_rotated(), guard.visited, has_exited=True)

    obstacle_hit = obstacles_hit[0]
    if (obstacle_hit, direction.coord) in guard.objects_hit_and_direction:
        return GuardState(pos, direction, guard.visited, is_looping=True)
    guard.objects_hit_and_direction.append((obstacle_hit, direction.coord))
    new_pos_list = copy(list(obstacle_hit))
    new_pos_list[direction.distance_indexer] -= direction.sign
    new_pos = (new_pos_list[0], new_pos_list[1])
    guard.visited.update(get_visit_set(pos, new_pos, direction))
    return GuardState(
        new_pos,
        direction.get_rotated(),
        guard.visited,
        objects_hit_and_direction=guard.objects_hit_and_direction,
    )


def solve1(guard: GuardState, obstacles: list[Coord], side_length: int) -> set[Coord]:
    while not guard.has_exited:
        guard = update_guard_state(guard, obstacles, side_length)
    return guard.visited


def check_if_cycle(guard: GuardState, obstacles: list[Coord], side_length: int) -> bool:
    while not (guard.has_exited or guard.is_looping):
        guard = update_guard_state(guard, obstacles, side_length)
    return guard.is_looping


def solve2(guard: GuardState, obstacles: list[Coord], side_length: int, visited: set[Coord]) -> int:
    visited.remove(guard.position)
    cycle_count = sum(
        # Nothing says I have a good algorithm like n_jobs=-1...
        Parallel(n_jobs=-1)(
            delayed(check_if_cycle)(deepcopy(guard), obstacles + [coord], side_length) for coord in tqdm(visited)
        )
    )
    return cycle_count


def main() -> None:
    maze, start, side_length = read_input(Path("data/input06.txt"))
    start_guard = GuardState(start, Direction((-1, 0)))
    visited = solve1(start_guard, maze, side_length)
    print(len(visited))
    print(solve2(GuardState(start, Direction((-1, 0))), maze, side_length, visited))


if __name__ == "__main__":
    main()

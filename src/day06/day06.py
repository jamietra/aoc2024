import itertools
from copy import copy
from math import sumprod
from pathlib import Path

Coord = tuple[int, int]


class Direction:
    def __init__(self, coord: Coord) -> None:
        self._rotation_matrix = [[0, 1], [-1, 0]]
        self.coord: tuple[int, int] = coord

    def get_rotated(self) -> "Direction":
        return Direction(
            (int(sumprod(self._rotation_matrix[0], self.coord)), int(sumprod(self._rotation_matrix[1], self.coord)))
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


def solve(pos: Coord, obstacles: list[Coord], direction: Direction, side_length: int, part2: bool) -> set[Coord] | bool:
    steps = 0
    spots_visited: set[Coord] = set()
    obstacles_hit_and_directions: list[tuple[Coord, Coord]] = []
    while True:
        obstacles = sorted(obstacles, key=lambda o: abs(o[0] - pos[0]) + abs(o[1] - pos[1]))
        obstacles_hit = list(
            itertools.dropwhile(
                lambda o: (pos[direction.collision_indexer] != o[direction.collision_indexer])
                or ((o[direction.distance_indexer] - pos[direction.distance_indexer]) * direction.sign < 0),
                obstacles,
            )
        )
        if not obstacles_hit:
            if part2:
                return False
            new_pos_list = [0, 0]
            new_pos_list[direction.collision_indexer] = pos[direction.collision_indexer]
            if direction.sign > 0:
                new_pos_list[direction.distance_indexer] = side_length - 1
            else:
                new_pos_list[direction.distance_indexer] = 0
            new_pos = (new_pos_list[0], new_pos_list[1])
            spots_visited.update(get_visit_set(pos, new_pos, direction))
            break

        obstacle_hit = obstacles_hit[0]
        if part2:
            if (obstacle_hit, direction.coord) in obstacles_hit_and_directions:
                return True
        obstacles_hit_and_directions.append((obstacle_hit, direction.coord))

        new_pos_list = copy(list(obstacle_hit))
        new_pos_list[direction.distance_indexer] -= direction.sign
        new_pos = (new_pos_list[0], new_pos_list[1])
        spots_visited.update(get_visit_set(pos, new_pos, direction))
        direction = direction.get_rotated()
        pos = new_pos
        steps += 1
    return spots_visited


def main() -> None:
    maze, start, side_length = read_input(Path("data/input06.txt"))
    visited = solve(start, maze, Direction((-1, 0)), side_length, False)
    print(len(visited))
    import time

    start_time = time.perf_counter()
    cycle_spots = 0
    iterations = 0
    for coord in visited:
        if coord == start:
            continue
        cycle_spots += solve(start, maze + [coord], Direction((-1, 0)), side_length, True)
        iterations += 1
        if iterations % 500 == 0:
            print((time.perf_counter() - start_time) / iterations)
            print(iterations / len(visited))
    print(cycle_spots)
    print(time.perf_counter() - start_time)


if __name__ == "__main__":
    main()

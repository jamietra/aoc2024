import math
from pathlib import Path


class Robot:

    def __init__(self, p: tuple[int, int], v: tuple[int, int], side_lengths: tuple[int, int]) -> None:
        self.p = p
        self.v = v
        self.side_lengths = side_lengths

    def update_position(self) -> None:
        self.p = ((self.p[0] + self.v[0]) % self.side_lengths[0], (self.p[1] + self.v[1]) % self.side_lengths[1])


def parse_input(path: Path, side_legnths: tuple[int, int]) -> list[Robot]:
    with open(path) as f:
        lines = f.read().splitlines()

    robot_list = []
    for line in lines:
        split_line = line.split(" ")
        position_split = split_line[0].replace("p=", "").split(",")
        position = (int(position_split[0]), int(position_split[1]))
        velocity_split = split_line[1].replace("v=", "").split(",")
        velocity = (int(velocity_split[0]), int(velocity_split[1]))
        robot_list.append(Robot(position, velocity, side_legnths))
    return robot_list


def get_quadrant_counts(robots: list[Robot], side_lengths: tuple[int, int]) -> list[int]:
    quadrant_counts = [0, 0, 0, 0]
    mid_points = (math.floor(side_lengths[0] / 2), math.floor(side_lengths[1] / 2))
    for r in robots:
        if r.p[0] < mid_points[0]:
            if r.p[1] < mid_points[1]:
                quadrant_counts[0] += 1
            if r.p[1] > mid_points[1]:
                quadrant_counts[1] += 1
        if r.p[0] > mid_points[0]:
            if r.p[1] < mid_points[1]:
                quadrant_counts[2] += 1
            if r.p[1] > mid_points[1]:
                quadrant_counts[3] += 1
    return quadrant_counts


def display_robots(robots: list[Robot], side_lengths: tuple[int, int], seconds: int) -> None:
    ps = [r.p for r in robots]
    counts = [[0 for _ in range(side_lengths[0])] for _ in range(side_lengths[1])]
    for p in ps:
        counts[p[1]][p[0]] += 1
    print(
        f"{seconds}\n"
        + "\n".join(list(map(lambda x: "".join(map(lambda y: f"{y:1d}" if y != 0 else " ", x)), counts))),
        end="\r",
        flush=True,
    )


def main() -> None:
    side_lengths = (101, 103)
    robots = parse_input(Path("data/input14.txt"), side_lengths)
    for _ in range(100):
        list(map(lambda x: x.update_position(), robots))
    print(math.prod(get_quadrant_counts(robots, side_lengths)))
    i = 0
    robots = parse_input(Path("data/input14.txt"), side_lengths)
    while True:
        i += 1
        list(map(lambda x: x.update_position(), robots))
        sf = math.prod(get_quadrant_counts(robots, side_lengths))
        if sf < 103860480:
            display_robots(robots, side_lengths, i)
            break


if __name__ == "__main__":
    main()

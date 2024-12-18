import functools
import math
from collections import OrderedDict
from pathlib import Path

from graph_utils import dijkstra, sort_distance_dict

type MazeNode = tuple[int, int, str]


def parse_maze(path: Path) -> list[list[str]]:
    with open(path) as f:
        lines = list(map(list, f.read().splitlines()))

    return lines


def find_node_locations(lines: list[list[str]]) -> tuple[list[MazeNode], list[MazeNode]]:
    """
    turn the parsed file into a list of all maze nodes and a list ends for accounting for different orientation
    """
    start = []
    locations = []
    end = []
    orientations = list(">v<^")

    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == ".":
                locations.extend([(i, j, orientation) for orientation in orientations])
            if char == "E":
                end.extend([(i, j, orientation) for orientation in orientations])
            if char == "S":
                start.extend([(i, j, orientation) for orientation in orientations])
    return start + locations + end, end


def create_distance_dict(locations: list[MazeNode]) -> OrderedDict[MazeNode, float]:
    distances = OrderedDict({node: math.inf for node in locations})
    distances[locations[0]] = 0
    return sort_distance_dict(distances)


def get_forward_and_rotational_neighbours(
    current_distance: float, current_node: MazeNode, unvisited_set: set[MazeNode]
) -> dict[MazeNode, float]:
    neighbours: dict[MazeNode, float] = {}
    neighbours |= get_forward_backward_node(current_distance, current_node, unvisited_set)
    neighbours |= get_rotation_neighbours(current_distance, current_node, unvisited_set)
    return neighbours


def get_forward_backward_node(
    current_distance: float, current_node: MazeNode, unvisited_set: set[MazeNode]
) -> dict[MazeNode, float]:
    """
    Helper function to find the neighbour accessible by moving forward in current orientation.
    """
    orientation_to_indexer_and_sign = {">": (1, 1), "v": (0, 1), "<": (1, -1), "^": (0, -1)}
    current_orientation = current_node[-1]
    indexer, sign = orientation_to_indexer_and_sign[current_orientation]
    current_position = [current_node[0], current_node[1]]
    current_position[indexer] += sign
    forward_node = (current_position[0], current_position[1], current_node[2])
    neighbours: dict[MazeNode, float] = {}
    if forward_node in unvisited_set:
        neighbours[forward_node] = 1.0 + current_distance
    return neighbours


def get_rotation_neighbours(
    current_distance: float, current_node: MazeNode, unvisited_set: set[MazeNode]
) -> dict[MazeNode, float]:
    """
    Get neighbours and their edge length for rotating 90 degrees clockwise and counter clockwise
    """
    orientation_to_degree = {">": 90, "v": 180, "<": 270, "^": 0}
    degree_to_orientation = {90: ">", 180: "v", 270: "<", 0: "^"}
    current_orientation = current_node[-1]
    current_degree = orientation_to_degree[current_orientation]
    return {
        new_node: current_distance + 1000
        for rotation in [-90, 90]
        if (new_node := (current_node[0], current_node[1], degree_to_orientation[(current_degree + rotation) % 360]))
        in unvisited_set
    }


def backtrack(
    current_point: MazeNode,
    node_to_previous: dict[MazeNode, set[MazeNode]],
    optimal_set: set[MazeNode],
    start: MazeNode,
) -> set[MazeNode]:
    """
    Iterate through the previous neighbour mapping to determine all tiles visited
    """
    optimal_set.add(current_point)
    if current_point == start:
        return optimal_set
    # noinspection PyTypeChecker
    return functools.reduce(
        set.union, [backtrack(n, node_to_previous, optimal_set, start) for n in node_to_previous[current_point]], set()
    )


def main() -> None:
    # maze = parse_maze(Path("data/sample16-2.txt"))
    maze = parse_maze(Path("data/input16.txt"))
    locations, ends = find_node_locations(maze)
    distances = create_distance_dict(locations)
    start = locations[0]
    start_correct_orientation = (start[0], start[1], ">")
    solved, visited = dijkstra(distances, get_forward_and_rotational_neighbours)
    end = [(n, dist) for n, dist in solved.items() if n in ends][-1]
    print(end)

    print(len(set([(x[0], x[1]) for x in backtrack(end[0], visited, set(), start_correct_orientation)])))


if __name__ == "__main__":
    main()

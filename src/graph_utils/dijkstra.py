from collections import OrderedDict, defaultdict
from queue import PriorityQueue
from typing import Callable

type Coord = tuple[int, int]


def dijkstra[
    NodeType
](
    distances: OrderedDict[NodeType, float],
    neighbour_getter: Callable[[float, NodeType, set[NodeType]], dict[NodeType, float]],
) -> tuple[OrderedDict[NodeType, float], dict[NodeType, set[NodeType]]]:
    """
    Run Dijkstra's algorithm to create a distance mapping and previous mapping to reconstruct paths to end
    """
    unvisited_set = set(distances.keys())
    unvisited: PriorityQueue[tuple[float, NodeType]] = PriorityQueue()
    for node, dist in distances.items():
        unvisited.put((dist, node))
    previous: defaultdict[NodeType, set[NodeType]] = defaultdict(set)
    while True:
        if not unvisited_set:
            return sort_distance_dict(distances), previous
        _, current_node = unvisited.get()
        # Hack to deal with this priority queue not having an update method. If it's priority has been updated with
        # alt_distance it will show up before the old entry in the queue and get removed from unvisited set, so we can
        # skip safely skip and not worry about updating
        if current_node not in unvisited_set:
            continue
        unvisited_set.remove(current_node)
        current_distance = distances[current_node]
        neighbours: dict[NodeType, float] = neighbour_getter(current_distance, current_node, unvisited_set)
        for node, alt_distance in neighbours.items():
            current_distance = distances[node]
            if alt_distance <= current_distance:
                distances[node] = min(distances[node], alt_distance)
                if alt_distance < current_distance:
                    previous[node] = {current_node}
                    unvisited.put((alt_distance, node))
                else:
                    previous[node].add(current_node)
    return sort_distance_dict(distances), previous


def sort_distance_dict[NodeType](distances: OrderedDict[NodeType, float]) -> OrderedDict[NodeType, float]:
    return OrderedDict(sorted(distances.items(), key=lambda x: x[-1], reverse=True))


def get_neighbours(
    current_distance: float,
    current_position: Coord,
    unvisted_set: set[Coord],
    obstacles: set[Coord],
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
        if x not in obstacles and x in unvisted_set and x[0] in range(max_row + 1) and x[1] in range(max_col + 1)
    }

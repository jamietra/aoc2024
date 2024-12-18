from collections import OrderedDict, defaultdict
from queue import PriorityQueue
from typing import Callable


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

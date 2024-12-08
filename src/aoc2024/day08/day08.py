import itertools
from collections import defaultdict
from pathlib import Path
from typing import Callable

Coord = tuple[int, int]
AntinodeFinder = Callable[[Coord, Coord, int], list[Coord]]


def parse_input(path: Path) -> tuple[defaultdict[str, list[Coord]], int]:
    """
    Create a mapping of node frequencies (single character) to a list of coordinates based on input file
    """
    with open(path) as f:
        lines = list(map(lambda s: s.strip(), f.readlines()))
    antenna_map: defaultdict[str, list[Coord]] = defaultdict(list)
    for i, row in enumerate(lines):
        for j, character in enumerate(row):
            if character != ".":
                antenna_map[character].append((i, j))
    return antenna_map, len(lines)


def get_antinode_location(antenna1: Coord, antenna2: Coord, map_size: int) -> list[Coord]:
    """
    Given the coordinates of two antennas return a list (always of length one but still a list for compatibility's sake)
    of the antinode location ignoring resonant harmonics. Note that we only look in one direction since
    `AntinodeFinders` are called on permutations of antenna pairs.
    """
    location = (antenna1[0] + (antenna1[0] - antenna2[0]), antenna1[1] + (antenna1[1] - antenna2[1]))
    if all((coord in range(map_size) for coord in location)):
        return [location]
    return []


def get_antinode_locations_with_resonant_harmonics(antenna1: Coord, antenna2: Coord, map_size: int) -> list[Coord]:
    """
    Given two antennas of the same frequency, return a list of all antinode coordinates accounting for resonant
    harmonics.
    """
    distance_vectors = antenna1[0] - antenna2[0], antenna1[1] - antenna2[1]
    antinodes = list(
        itertools.takewhile(
            lambda coord: coord[0] in range(map_size) and coord[1] in range(map_size),
            ((antenna1[0] + i * distance_vectors[0], antenna1[1] + i * distance_vectors[1]) for i in range(map_size)),
        )
    )
    return antinodes


def solve_parts(antenna_map: defaultdict[str, list[Coord]], map_size: int, finders: list[AntinodeFinder]) -> list[int]:
    """
    given a map of antennas, maximum coordinate value, and a list of `AntinodeFinders` return a list where each entry
    is the number of unique antinode locations for the respective finder.
    """
    finder_index_to_locations: defaultdict[int, set[Coord]] = defaultdict(set)
    for _, coords in antenna_map.items():
        for i, f in enumerate(finders):
            loc_set = set(
                itertools.chain.from_iterable(
                    map(
                        lambda perm: f(perm[0], perm[1], map_size),
                        itertools.permutations(coords, 2),
                    )
                )
            )
            finder_index_to_locations[i] |= loc_set
    return [len(locs) for locs in finder_index_to_locations.values()]


def main() -> None:
    antenna_map, map_size = parse_input(Path("data/input08.txt"))
    results = solve_parts(
        antenna_map, map_size, [get_antinode_location, get_antinode_locations_with_resonant_harmonics]
    )
    print(results[0])
    print(results[1])


if __name__ == "__main__":
    main()

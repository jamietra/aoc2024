import itertools
from collections import deque
from pathlib import Path
from typing import Protocol

from tqdm import tqdm

# Tuple with index of data group and tuple of len(file) with file ids as values.
# Using tuple so it can be removed from deque
IndexAndGroup = tuple[int, tuple[int, ...]]
DiskMap = list[int | str]


def read_disk_map(path: Path) -> str:
    with open(path) as f:
        line = f.read().strip()
    return line


class PartHandler(Protocol):

    def handle_character(self, index: int, space_length: int, defragged: DiskMap) -> DiskMap: ...


class Part1Handler:

    def __init__(self, data_groups: list[IndexAndGroup], line_length: int) -> None:
        self.data_queue = deque((list(itertools.chain.from_iterable(map(lambda g: g[1], data_groups)))))
        self.indices_to_fill = set(range(1, line_length, 2))

    def handle_character(self, index: int, space_length: int, defragged: DiskMap) -> DiskMap:
        id_count = min(space_length, len(self.data_queue))
        if index in self.indices_to_fill:
            defragged.extend([self.data_queue.pop() for _ in range(id_count)])
        else:
            defragged.extend([self.data_queue.popleft() for _ in range(id_count)])
        return defragged


class Part2Handler:
    def __init__(self, data_groups: list[IndexAndGroup], line_length: int) -> None:
        self.group_deque = deque(data_groups)
        self.indices_to_fill = set(range(1, line_length, 2))

    def handle_character(self, index: int, space_length: int, defragged: DiskMap) -> DiskMap:
        if index in self.indices_to_fill:
            self.group_deque.reverse()
            filler = self.fill_gap(space_length)
            self.group_deque.reverse()
            self.indices_to_fill |= set([f[0] for f in filler])
            fill_data: DiskMap = list(itertools.chain.from_iterable([f[1] for f in filler]))
            fill_data += (space_length - len(fill_data)) * ["."]
            defragged.extend(fill_data)
        else:
            defragged.extend(list(self.group_deque.popleft()[1]))
        return defragged

    def fill_gap(self, gap_length: int) -> list[IndexAndGroup]:
        """
        Given length of empty space to fill and deque of files in order to fill in return a list of IndexAndGroups to
        fill in the empty space with and remove these files from the deque.
        """
        if gap_length == 0:
            return []
        # get the first occurrence that isn't too long without iterating the entire list.
        # Would just be head $ dropWhile in haskell
        try:
            next_file = next(itertools.dropwhile(lambda g: len(g[1]) > gap_length, self.group_deque))
        except StopIteration:
            return []
        self.group_deque.remove(next_file)
        return [next_file] + self.fill_gap(gap_length - len(next_file[1]))


def check_sum(disk_map: DiskMap) -> int:
    return sum([i * char for i, char in enumerate(disk_map) if isinstance(char, int)])


def main() -> None:
    line = read_disk_map(Path("data/input09.txt"))
    data_groups = [(i, tuple(int(line[i]) * [i // 2])) for i in range(0, len(line), 2)]
    handlers: list[PartHandler] = [Part1Handler(data_groups, len(line)), Part2Handler(data_groups, len(line))]
    disk_maps: list[DiskMap] = [[], []]

    for i, char in tqdm(enumerate(line)):
        for j, h in enumerate(handlers):
            disk_maps[j] = h.handle_character(i, int(char), disk_maps[j])

    print(check_sum(disk_maps[0]))
    print(check_sum(disk_maps[1]))


if __name__ == "__main__":
    main()

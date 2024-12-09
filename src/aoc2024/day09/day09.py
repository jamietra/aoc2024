import itertools
from collections import deque
from pathlib import Path

from tqdm import tqdm

# Tuple with index of data group and tuple of len(file) with file ids as values.
# Using tuple so it can be removed from deque
IndexAndGroup = tuple[int, tuple[int, ...]]
DiskMap = list[int | str]


def read_disk_map(path: Path) -> str:
    with open(path) as f:
        line = f.read().strip()
    return line


def fill_gap(group_deque: deque[IndexAndGroup], gap_length: int) -> list[IndexAndGroup]:
    """
    Given length of empty space to fill and deque of files in order to fill in return a list of IndexAndGroups to fill
    in the empty space with and remove these files from the deque.
    """
    if gap_length == 0:
        return []
    try:
        next_file = next(itertools.dropwhile(lambda g: len(g[1]) > gap_length, group_deque))
    except StopIteration:
        return []
    # Eww side effect
    group_deque.remove(next_file)
    result = [next_file] + fill_gap(group_deque, gap_length - len(next_file[1]))
    return result


def main() -> None:
    line = read_disk_map(Path("data/input09.txt"))
    data_groups = [(i, tuple(int(line[i]) * [i // 2])) for i in range(0, len(line), 2)]
    group_deque: deque[IndexAndGroup] = deque(data_groups)
    data_queue: deque[int] = deque((list(itertools.chain.from_iterable(map(lambda g: g[1], data_groups)))))
    compressed: DiskMap = []
    compressed2: DiskMap = []

    part1_indices_to_fill: set[int] = set(range(1, len(line), 2))
    part2_indices_to_fill: set[int] = set(range(1, len(line), 2))
    for i, char in tqdm(enumerate(line)):
        f_length = int(char)
        id_count = min(len(data_queue), f_length)
        if len(group_deque) == 0:
            break
        if i in part1_indices_to_fill:
            compressed.extend([data_queue.pop() for _ in range(id_count)])
        else:
            compressed.extend([data_queue.popleft() for _ in range(id_count)])
        if i in part2_indices_to_fill:
            group_deque.reverse()
            filler = fill_gap(group_deque, f_length)
            group_deque.reverse()
            part2_indices_to_fill |= set([f[0] for f in filler])
            fill_data: DiskMap = list(itertools.chain.from_iterable([f[1] for f in filler]))
            fill_data += (f_length - len(fill_data)) * ["."]
            compressed2.extend(fill_data)
        else:
            compressed2.extend(list(group_deque.popleft()[1]))

    print(sum([i * char for i, char in enumerate(compressed) if isinstance(char, int)]))
    print(sum([i * char for i, char in enumerate(compressed2) if isinstance(char, int)]))


if __name__ == "__main__":
    main()

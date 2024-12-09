from collections import deque
import itertools
from pathlib import Path
import re

from tqdm import tqdm


def old_solve():
    pass
    # for i, character in enumerate(files):
    #     if file_space_needed <= 1:
    #         disk_map += reversed_expanded_files[: int(spaces[i])]
    #         break
    #
    #     next_characters = (int(character) * str(i) + reversed_expanded_files[: int(spaces[i])])[:file_space_needed]
    #     file_space_needed -= len(next_characters)
    #     disk_map += next_characters
    #     reversed_expanded_files = reversed_expanded_files[int(spaces[i]) :]
    #     # else:
    #     #     disk_map +=


def read_disk_map(path: Path) -> str:
    with open(path) as f:
        line = f.read().strip()
    return line


def check_map(disk_map: str) -> bool:
    return not any(re.finditer(r"\d\.+\d", disk_map))


def fill_gap(group_deque: deque[tuple[int, tuple[int, ...]]], gap_length: int) -> list[tuple[int, tuple[int, ...]]]:
    if gap_length == 0:
        return []
    try:
        next_file = next(itertools.dropwhile(lambda g: len(g[1]) > gap_length, group_deque))
    except StopIteration:
        return []

    group_deque.remove(next_file)
    result = [next_file] + fill_gap(group_deque, gap_length - len(next_file[1]))
    return result


def fill_in_missing_gap(
    group_deque: deque[tuple[int, tuple[int, ...]]],
    gap_length: int,
    new_empty_indices: list[int],
    compressed: list[int | str],
) -> list[int | str]:
    group_deque.reverse()
    filler = fill_gap(group_deque, gap_length)
    group_deque.reverse()
    new_empty_indices.extend([f[0] for f in filler])
    fill_data = list(itertools.chain.from_iterable([f[1] for f in filler]))
    fill_data += (gap_length - len(fill_data)) * ["."]
    compressed.extend(fill_data)
    return compressed


def main():
    # line = read_disk_map(Path("data/sample09.txt"))
    line = read_disk_map(Path("data/input09.txt"))
    data_groups = [(i, tuple(int(line[i]) * [i // 2])) for i in range(0, len(line), 2)]
    group_deque = deque(data_groups)
    data_queue = deque((list(itertools.chain.from_iterable(map(lambda g: g[1], data_groups)))))
    compressed = []
    compressed2 = []
    new_empty = []
    for i, char in tqdm(enumerate(line)):
        f_length = int(char)
        id_count = min(len(data_queue), f_length)
        if len(group_deque) == 0:
            break
        if i % 2 == 0:
            compressed.extend([data_queue.popleft() for _ in range(id_count)])
            if i not in new_empty:
                compressed2.extend(list(group_deque.popleft()[1]))
            else:
                compressed2 = fill_in_missing_gap(group_deque, f_length, new_empty, compressed2)
        else:
            compressed.extend([data_queue.pop() for _ in range(id_count)])
            compressed2 = fill_in_missing_gap(group_deque, f_length, new_empty, compressed2)
    print(sum([i * char for i, char in enumerate(compressed) if char != "."]))
    print(sum([i * char for i, char in enumerate(compressed2) if char != "."]))


def main1():
    # line = read_disk_map(Path("data/sample09.txt"))
    line = read_disk_map(Path("data/input09.txt"))
    files = [line[i] for i in range(0, len(line), 2)]
    spaces = [line[i] for i in range(1, len(line), 2)]
    disk_map = []
    for i, character in enumerate(line):
        if i % 2 == 0:
            disk_map.extend(int(character) * [i // 2])
        else:
            disk_map.extend(int(character) * ["."])
    # disk_map = list(
    #     itertools.chain.from_iterable(
    #         [int(files[i]) * [i] + int(spaces[i]) * ["."] for i in range(max(len(files), len(spaces)))]
    #     )
    # )
    reversed_expanded_files = list(reversed([x for x in disk_map if x != "."]))
    print(list(map(lambda x: f"{x:4d}" if isinstance(x, int) else "....", disk_map))[-50:])
    current_index = 0
    for k, group in tqdm(itertools.groupby(disk_map)):
        group = list(group)
        group_length = len(group)
        new_index = current_index + group_length
        if k != ".":
            last_num = k
        if k == ".":
            if reversed_expanded_files[0] <= last_num:
                break
            tail = disk_map[new_index:-group_length]
            tail = list(reversed(list(itertools.dropwhile(lambda x: x == ".", reversed(tail)))))
            disk_map = disk_map[:current_index] + reversed_expanded_files[:group_length] + tail
            if disk_map[-1] == ".":
                disk_map.pop()
            # if check_map("".join(map(str, disk_map))):
            #     break
            reversed_expanded_files = reversed_expanded_files[group_length:]
        current_index = new_index
    print(list(map(lambda x: f"{x:4d}" if isinstance(x, int) else "....", disk_map))[-50:])
    print(sum([i * char for i, char in enumerate(disk_map) if char != "."]))


if __name__ == "__main__":
    main1()

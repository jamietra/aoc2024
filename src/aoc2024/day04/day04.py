import itertools
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, DefaultDict, Generator, Iterable


def read_input(path: Path) -> list[str]:
    with open(path) as f:
        words = f.read().strip().split("\n")
    return words


@dataclass
class WordSearch:
    matrix: list[str]

    rows: int = field(init=False)
    cols: int = field(init=False)

    def __post_init__(self) -> None:
        self.rows = len(self.matrix)
        self.cols = len(self.matrix[0])

    def get(self, row: int, col: int) -> str:
        return self.matrix[row][col]

    def locations(self, character: str) -> list[tuple[int, int]]:
        locations = []
        for line_no, line in enumerate(self.matrix):
            for col_no, char in enumerate(line):
                if char == character:
                    locations.append((line_no, col_no))
        return locations

    def _get_directions(self, start: tuple[int, int], next_: tuple[int, int]) -> tuple[int, int]:
        r_start, c_start = start
        r_next, c_next = next_
        return r_next - r_start, c_next - c_start

    def count_word_occurences(self, word: str) -> int:
        start_locations = self.locations(word[0])
        found_count = 0
        start_to_directions: DefaultDict[tuple[int, int], list[tuple[int, int]]] = defaultdict(list)
        for start in start_locations:
            start_to_directions[start].extend(
                map(lambda x: self._get_directions(start, x), self.locations_from_neighbours(start, word[1]))
            )

        for start, directions in start_to_directions.items():
            if not directions:
                continue
            possible_words = map(lambda d: self._get_sequence_from_direction(start, d, len(word)), directions)
            found_count += len([w for w in possible_words if w == word])
        return found_count

    def _get_sequence_from_direction(self, start: tuple[int, int], direction: tuple[int, int], length: int) -> str:
        r_start, c_start = start
        r_direction, c_direction = direction
        r_range = [r_start] if r_direction == 0 else range(r_start, r_start + r_direction * length, r_direction)
        c_range = [c_start] if c_direction == 0 else range(c_start, c_start + c_direction * length, c_direction)
        fill_value = r_start if r_direction == 0 else c_start
        return "".join(
            [
                self.get(*coord)
                for coord in itertools.takewhile(
                    lambda c: not self.is_out_of_bounds(*c),
                    itertools.zip_longest(r_range, c_range, fillvalue=fill_value),
                )
            ]
        )

    def _get_range(self, start: int, max_val: int) -> Iterable[int]:
        return range(max(start - 1, 0), min(start + 2, max_val))

    def locations_from_neighbours(
        self, start: tuple[int, int], character: str
    ) -> Generator[tuple[int, int], Any, None]:
        row, col = start

        row_range = self._get_range(row, self.rows)
        col_range = self._get_range(col, self.cols)
        neighbour_coords = [coord for coord in itertools.product(row_range, col_range) if coord != start]
        return (coord for coord in neighbour_coords if self.get(*coord) == character)

    def is_out_of_bounds(self, row: int, col: int) -> bool:
        return row < 0 or col < 0 or row >= self.rows or col >= self.cols

    def get_valid_diagonals(self, row: int, col: int) -> Generator[tuple[int, int], Any, None]:
        return (
            coord
            for coord in itertools.product((row - 1, row + 1), (col - 1, col + 1))
            if not self.is_out_of_bounds(*coord)
        )


def main() -> None:
    words = read_input(Path("data/input04.txt"))

    puzzle = WordSearch(words)
    print(puzzle.count_word_occurences("XMAS"))
    a_locations = puzzle.locations("A")
    first_pass = []
    for row_loc, col_loc in a_locations:
        diagonals = itertools.product((row_loc - 1, row_loc + 1), (col_loc - 1, col_loc + 1))
        for new_row, new_col in diagonals:
            if puzzle.is_out_of_bounds(new_row, new_col):
                break
            if puzzle.get(new_row, new_col) not in "MS":
                break
        else:
            first_pass.append((row_loc, col_loc))
    second_pass = []
    for row, col in first_pass:
        first_diag = "".join(
            [puzzle.get(row + r_offset, col + c_offset) for (r_offset, c_offset) in [(-1, 1), (1, -1)]]
        )
        second_diag = "".join(
            [puzzle.get(row + r_offset, col + c_offset) for (r_offset, c_offset) in [(1, 1), (-1, -1)]]
        )
        if first_diag not in [
            "SM",
            "MS",
        ]:
            continue
        elif second_diag not in [
            "SM",
            "MS",
        ]:
            continue
        else:
            second_pass.append((row, col))
    print(len(second_pass))


if __name__ == "__main__":
    main()

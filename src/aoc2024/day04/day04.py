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
    """
    Probably should've just made diagonal/transpose/reverse accessors instead of doing this adhoc serch stuff...
    """

    matrix: list[str]

    rows: int = field(init=False)
    cols: int = field(init=False)

    def __post_init__(self) -> None:
        self.rows = len(self.matrix)
        self.cols = len(self.matrix[0])

    def get(self, row: int, col: int) -> str:
        return self.matrix[row][col]

    def locations(self, character: str) -> list[tuple[int, int]]:
        """
        Get all coordinates of given character
        """
        locations = []
        for line_no, line in enumerate(self.matrix):
            for col_no, char in enumerate(line):
                if char == character:
                    locations.append((line_no, col_no))
        return locations

    def _get_directions(self, start: tuple[int, int], next_: tuple[int, int]) -> tuple[int, int]:
        """
        helper to get a tuple of direction given two points
        """
        r_start, c_start = start
        r_next, c_next = next_
        return r_next - r_start, c_next - c_start

    def count_word_occurences(self, word: str) -> int:
        """
        Search the word search and count
        """
        # Maybe add functionality for getting tuples
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

    def get_crossword_centroids(self, word: str) -> list[tuple[int, int]]:
        """
        Find all "cross" words (or is it X words...) of the given word and return a list of their centroids
        """
        word = word.upper()
        if len(word) % 2 != 1 or len(word) < 3:
            raise ValueError("len of word must be an odd number greater than 3")

        middle_point = len(word) // 2
        middle_letter = word[middle_point]
        first_half = word[:middle_point]
        second_half = word[(middle_point + 1) :]
        other_letters = first_half + second_half
        reversed_others = other_letters[::-1]
        centers = self.locations(middle_letter)
        cross_centers = []
        for row, col in centers:
            neighbours = itertools.takewhile(
                lambda coord: not self.is_out_of_bounds(*coord) and (self.get(*coord) in other_letters),
                self.get_all_diagonals(row, col),
            )
            if len(list(neighbours)) < 2 * len(other_letters):
                continue
            down_diag = "".join(
                [self.get(row + r_offset, col + c_offset) for (r_offset, c_offset) in [(1, 1), (-1, -1)]]
            )
            if down_diag not in [other_letters, reversed_others]:
                continue
            up_diag = "".join([self.get(row + r_offset, col + c_offset) for (r_offset, c_offset) in [(-1, 1), (1, -1)]])
            if up_diag not in [other_letters, reversed_others]:
                continue
            cross_centers.append((row, col))
        return cross_centers

    def _get_sequence_from_direction(self, start: tuple[int, int], direction: tuple[int, int], length: int) -> str:
        """
        Given a start, direction, and length return that string
        """
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
        """
        helper to get a boundary aware range
        """
        return range(max(start - 1, 0), min(start + 2, max_val))

    def locations_from_neighbours(
        self, start: tuple[int, int], character: str
    ) -> Generator[tuple[int, int], Any, None]:
        """
        Get coordinates of letters adjacent to `start` and return a list of their coordinates
        """
        row, col = start

        row_range = self._get_range(row, self.rows)
        col_range = self._get_range(col, self.cols)
        neighbour_coords = [coord for coord in itertools.product(row_range, col_range) if coord != start]
        return (coord for coord in neighbour_coords if self.get(*coord) == character)

    def is_out_of_bounds(self, row: int, col: int) -> bool:
        return row < 0 or col < 0 or row >= self.rows or col >= self.cols

    def get_all_diagonals(self, row: int, col: int) -> Generator[tuple[int, int], Any, None]:
        """
        This is called in the crossword finder so that it can early exit using takewhile
        """
        return (coord for coord in itertools.product((row - 1, row + 1), (col - 1, col + 1)))

    def get_valid_diagonals(self, row: int, col: int) -> Generator[tuple[int, int], Any, None]:
        return (coord for coord in self.get_all_diagonals(row, col) if not self.is_out_of_bounds(*coord))


def main() -> None:
    words = read_input(Path("data/input04.txt"))
    puzzle = WordSearch(words)
    print(puzzle.count_word_occurences("XMAS"))
    new_crosses = puzzle.get_crossword_centroids("MAS")
    print(len(new_crosses))


if __name__ == "__main__":
    main()

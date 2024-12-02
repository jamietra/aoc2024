import itertools
from copy import copy
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Protocol

RowOperator = Callable[[int, int], int]
ColumnOperator = Callable[[list[int], list[int]], list[int]]
Aggregator = Callable[[list[int]], int]
Rows = list[tuple[int, int]]
Columns = tuple[list[int], list[int]]


class Day1Problem(Protocol):

    def solve(self) -> int: ...


@dataclass
class RowWiseProblem:
    data_path: Path
    row_operator: RowOperator
    aggregator: Aggregator

    def solve(self) -> int:
        return row_wise_aggregation(read_sorted_day1_rows(self.data_path), self.row_operator, self.aggregator)


@dataclass
class ColumnWiseProblem:
    data_path: Path
    column_operator: ColumnOperator
    aggregator: Aggregator

    def solve(self) -> int:
        return column_wise_aggregation(read_sorted_day1_columns(self.data_path), self.column_operator, self.aggregator)


def read_day1_lines(data_path: Path) -> list[str]:
    """
    Strip and split input file into lines.
    """
    with open(data_path) as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    return lines


def read_sorted_day1_columns(data_path: Path) -> Columns:
    """
    Get a tuple of the left and right column in the input data that are sorted in ascending order
    """
    rows = [(int((row := line.split())[0]), int(row[1])) for line in read_day1_lines(data_path)]
    columns = rows_to_sorted_columns(rows)
    return columns


def read_sorted_day1_rows(data_path: Path) -> Rows:
    """
    Get a list of row tuples after sorting each column individually
    """
    columns = read_sorted_day1_columns(data_path)
    # Again zips typing not parameterized correctly
    rows = [(left, right) for left, right in zip(*columns)]
    return rows


def rows_to_sorted_columns(rows: Rows) -> Columns:
    """
    Ideally this would just tuple(zip(*rows)) but that introduces an ANY type which is unacceptable
    """
    return sorted([row[0] for row in rows]), sorted([row[1] for row in rows])


def distance_row_operator(left_value: int, right_value: int) -> int:
    """
    Calculate the euclidean distance between `left_value` and `right_value`
    """
    return abs(left_value - right_value)


def sum_aggregator(values: list[int]) -> int:
    """
    Sum implementation of the `Aggregator` callable type
    """
    return sum(values)


def occurrence_counting_column_operator(left_col: list[int], right_col: list[int]) -> list[int]:
    """
    Take unique values from `left_col` and get a list of each value multiplied by how many times it occurs in `left_col`
    and by how many times it is in `right_col`.
    """
    # Ensure lists are sorted but copy so we don't modify the passed lists
    left_counts = get_occurrence_counts(sorted(copy(left_col)))
    right_counts = get_occurrence_counts(sorted(copy(right_col)))
    per_value_products = [
        left_key * left_val * right_counts.get(left_key, 0) for left_key, left_val in left_counts.items()
    ]
    return per_value_products


def get_occurrence_counts(column: list[int]) -> dict[int, int]:
    """
    Get a mapping of each unique value in `column` to the number of times it occurs
    """
    return {x: len(list(group)) for x, group in itertools.groupby(column)}


def row_wise_aggregation(rows: Rows, row_operation: RowOperator, aggregator: Aggregator) -> int:
    """
    Apply a row wise aggregation and then column wise aggregation
    """
    return aggregator([row_operation(left_value, right_value) for left_value, right_value in rows])


def column_wise_aggregation(
    columns: Columns,
    column_operation: ColumnOperator,
    aggregator: Aggregator,
) -> int:
    """
    Apply aggregation to tuple of columns
    """
    left_col, right_col = columns
    return aggregator(column_operation(left_col, right_col))


def solve_problem(problem: Day1Problem) -> int:
    return problem.solve()


def main() -> None:
    print(
        solve_problem(
            RowWiseProblem(
                Path("data/input01.txt"),
                distance_row_operator,
                sum_aggregator,
            )
        )
    )
    print(
        solve_problem(
            ColumnWiseProblem(
                Path("data/input01.txt"),
                occurrence_counting_column_operator,
                sum_aggregator,
            )
        )
    )


if __name__ == "__main__":
    main()

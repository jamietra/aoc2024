from pathlib import Path
from typing import Callable, Protocol


class Checkable(Protocol):
    @property
    def is_okay(self) -> bool: ...


class Part1Report(Checkable):
    """
    Implementation of report protocol with the `is_okay` property. This implementation is pre Problem Dampener so
    should probably be deprecated. Differences are pre-computed as they are used quite frequently
    """

    def __init__(self, data: list[int]):
        self.data = data
        self._report_length = len(data)
        self._differences = self._calculate_differences()

    def _calculate_differences(self) -> list[int]:
        return [self.data[i + 1] - self.data[i] for i in range(self._report_length - 1)]

    @property
    def _is_strict_monotonic(self) -> bool:
        return all(map(lambda level_diff: level_diff < 0, self._differences)) | all(
            map(lambda level_diff: level_diff > 0, self._differences)
        )

    @property
    def _max_absolute_difference(self) -> float:
        return max(map(abs, self._differences))

    @property
    def is_okay(self) -> bool:
        if not self._is_strict_monotonic:
            return False
        else:
            return self._max_absolute_difference <= 3


class Part2Report(Part1Report):
    """
    Implementation of report protocol with post Problem Dampener introduction
    """

    @property
    def is_okay(self) -> bool:
        if super().is_okay:
            return True
        else:
            return self._is_okay_with_removed_level

    @property
    def _is_okay_with_removed_level(self) -> bool:
        # Brute force since these are small, and it's the most readable solution
        for i in range(self._report_length):
            # Hit that early exit
            if Part1Report(self.data[:i] + self.data[i + 1 :]).is_okay:
                return True
        return False


def load_reports(path: Path) -> list[list[int]]:
    """
    Load and parse reports into lists of ints
    """
    with open(path) as f:
        report_data = list(map(lambda line: list(map(int, line.strip().split())), f.readlines()))

    return report_data


def create_report_objects(
    report_data: list[list[int]], report_factory: Callable[[list[int]], Checkable]
) -> list[Checkable]:
    """
    Load a list of report data into the given report types
    """
    return [report_factory(report) for report in report_data]


def count_okay_reports(reports: list[Checkable]) -> int:
    """
    Get the number of okay reports in a list
    """
    return sum([report.is_okay for report in reports])


def main() -> None:
    report_data = load_reports(Path("data/input02.txt"))

    part1_reports = create_report_objects(report_data, lambda x: Part1Report(x))
    part2_reports = create_report_objects(report_data, lambda x: Part2Report(x))
    print(count_okay_reports(part1_reports))
    print(count_okay_reports(part2_reports))


if __name__ == "__main__":
    main()

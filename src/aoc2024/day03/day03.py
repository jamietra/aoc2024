import itertools
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable, Optional

NumberPairs = list[tuple[float, float]]
Extractor = Callable[[str, str], NumberPairs]
PairOperator = Callable[[float, float], float]
Aggregator = Callable[[Iterable[float]], float]


@dataclass
class Day3Runner:
    """
    Solve a day 3 type problem with any extractor, pairwise operation, aggregation and command name. (Defaults to mul)
    """

    extractor: Extractor
    operation: PairOperator
    aggregation: Aggregator
    function_name: Optional[str] = "mul"
    pattern: str = field(init=False)

    def __post_init__(self) -> None:
        self.pattern = rf"{self.function_name}\(\d{{1,3}}\,\d{{1,3}}\)"

    def run(self, commands: str) -> float:
        return self.aggregation(map(lambda pair: self.operation(*pair), self.extractor(self.pattern, commands)))


def read_input(path: Path) -> str:
    with open(path) as f:
        commands = "".join(map(lambda x: x.strip(), f.readlines()))
    return commands


def extract_numbers_from_function_call(function_call: str) -> tuple[float, float]:
    """
    Turn something like "mul(69,420)" into the tuple `(69, 420)`
    """
    split = function_call.split("(")[1].strip(")").split(",")
    return int(split[0]), int(split[1])


def extract_numbers(pattern: str, commands: str) -> NumberPairs:
    """
    Apply the pattern assuming it will generate a list of strings the form "<func_name>(xxx, yyy)" when plugged into
    re.findall, then strip off the function part and return a list of number tuples
    """
    matches: list[str] = re.findall(pattern, commands)
    numbers = [extract_numbers_from_function_call(match) for match in matches]
    return numbers


def extract_numbers_in_dos(pattern: str, commands: str) -> NumberPairs:
    """
    Remove parts of the command string between `don't()...do()` and the extract number pairs using `extract_numbers()`
    """
    do_splits = commands.split("do()")
    actual_dos = "".join(itertools.chain.from_iterable([do_block.split("don't()")[0] for do_block in do_splits]))
    return extract_numbers(pattern, actual_dos)


def main() -> None:
    commands = read_input(Path("data/input03.txt"))
    part1 = Day3Runner(extract_numbers, lambda x, y: x * y, sum)
    part2 = Day3Runner(extract_numbers_in_dos, lambda x, y: x * y, sum)
    print(part1.run(commands))
    print(part2.run(commands))


if __name__ == "__main__":
    main()

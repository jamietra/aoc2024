from math import prod, sumprod
from pathlib import Path
from typing import Callable, Iterable

from joblib import Parallel, delayed

Equation = tuple[list[int], int]


def read_input(path: Path) -> list[Equation]:
    with open(path) as f:
        contents = f.read()

    lines = contents.strip().split("\n")
    equations = []
    for line in lines:
        split_line = list(map(lambda x: x.strip(), line.split(":")))

        equations.append((list(map(int, split_line[-1].split())), int(split_line[0])))
    return equations


def evaluate_equation(eq: Equation, operators: list[Callable[[Iterable[int]], int]]) -> bool:
    test_value = eq[1]
    input_values = eq[0]
    if len(input_values) == 1:
        return input_values[0] == test_value
    return any(
        [
            evaluate_equation(([operator(input_values[:2])] + input_values[2:], test_value), operators)
            for operator in operators
        ]
    )


def solve(equations: list[Equation], operators: list[Callable[[Iterable[int]], int]]) -> float:
    # noinspection PyTypeChecker
    # MyPy knows better than jetbrains
    plausible_mask = Parallel(n_jobs=-1)(delayed(evaluate_equation)(equation, operators) for equation in equations)
    return sumprod(plausible_mask, [equation[-1] for equation in equations])


def integer_concate(integers: Iterable[int]) -> int:
    return int("".join(map(str, integers)))


def main() -> None:
    equations = read_input(Path("data/input07.txt"))
    print(solve(equations, [sum, prod]))
    print(solve(equations, [sum, prod, integer_concate]))


if __name__ == "__main__":
    main()

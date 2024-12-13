import math
import re
from pathlib import Path


class Claw:
    def __init__(
        self,
        a_button: tuple[int, int],
        b_button: tuple[int, int],
        prize: tuple[int, int],
        max_per_button_presses: int | None,
    ) -> None:
        self.a_button = a_button
        self.b_button = b_button
        self.a_cost = 3
        self.b_cost = 1
        self.prize = prize
        self.max_per_button_presses = max_per_button_presses
        # doing the linear algerbra wrong
        self._determinant = self.a_button[0] * self.b_button[1] - self.b_button[0] * self.a_button[1]

    @property
    def can_get_prize(self) -> bool:
        return (
            (self.prize[0] % math.gcd(self.a_button[0], self.b_button[0])) == 0
            and ((self.prize[1] % math.gcd(self.a_button[1], self.b_button[1])) == 0)
            or self._determinant == 0
        )

    def min_cost(self) -> float:
        a_presses = (self.b_button[1] * self.prize[0] - self.b_button[0] * self.prize[1]) / self._determinant
        b_presses = (-self.a_button[1] * self.prize[0] + self.a_button[0] * self.prize[1]) / self._determinant
        if self.max_per_button_presses:
            if a_presses > self.max_per_button_presses or b_presses > self.max_per_button_presses:
                return 0
        # I don't understand why this is necessary but whatevs
        if not a_presses.is_integer() or not b_presses.is_integer():
            return 0
        return a_presses * self.a_cost + b_presses * self.b_cost


def parse_input(path: Path) -> list[list[tuple[int, int]]]:
    with open(path) as f:
        machines = f.read().split("\n\n")
    machine_list = []
    for m in machines:
        xs = list(map(int, re.findall(r"X[+=](\d+)", m)))
        ys = list(map(int, re.findall(r"Y[+=](\d+)", m)))
        machine_list.append([(xs[i], ys[i]) for i in range(3)])
    return machine_list


def check_machines(machines: list[Claw]) -> float:
    return sum([m.min_cost() for m in machines if m.can_get_prize])


def main() -> None:
    machines = parse_input(Path("data/input13.txt"))
    machines1 = [Claw(m[0], m[1], m[2], max_per_button_presses=100) for m in machines]
    print(check_machines(machines1))
    machines2 = [
        Claw(m[0], m[1], (m[2][0] + 10000000000000, m[2][1] + 10000000000000), max_per_button_presses=None)
        for m in machines
    ]
    print(check_machines(machines2))


if __name__ == "__main__":
    main()

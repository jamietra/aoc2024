import asyncio
import itertools
from asyncio import Queue
from collections import deque
from pathlib import Path
from typing import Callable

from tqdm import tqdm

type Program = list[int]


def weird_division(a: int, b: int) -> int:
    return int(a / (2**b))


class Computer:

    def __init__(self, ra: int, rb: int, rc: int) -> None:
        self.ra = deque([ra], maxlen=1)
        self.rb = deque([rb], maxlen=1)
        self.rc = deque([rc], maxlen=1)
        self.instruction_pointer = 0
        self.op_code_to_op: dict[int, Callable[[int], int | None]] = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }

    def combo_operand(self, combo_op: int) -> int:
        if combo_op == 7:
            raise ValueError("7 is a reserved combo operand")
        if combo_op <= 3:
            return combo_op
        combo_op_to_register = {4: self.ra, 5: self.rb, 6: self.rc}
        return combo_op_to_register[combo_op][0]

    def run_instruction(self, op_code: int, argument: int) -> int | None:
        return self.op_code_to_op[op_code](argument)

    def adv(self, combo_op: int) -> None:
        self.ra.append(weird_division(self.ra.pop(), self.combo_operand(combo_op)))
        self.instruction_pointer += 2

    def bxl(self, combo_op: int) -> None:
        self.rb.append(self.rb.pop() ^ combo_op)
        self.instruction_pointer += 2

    def bst(self, combo_op: int) -> None:
        self.rb.pop()
        self.rb.append(self.combo_operand(combo_op) % 8)
        self.instruction_pointer += 2

    def jnz(self, combo_op: int) -> None:
        if self.ra[0] == 0:
            self.instruction_pointer += 2
            return
        self.instruction_pointer = combo_op

    def bxc(self, combo_op: int) -> None:
        self.rb.append(self.rb.pop() ^ self.rc[0])
        self.instruction_pointer += 2

    def out(self, combo_op: int) -> int:
        self.instruction_pointer += 2
        return self.combo_operand(combo_op) % 8

    def bdv(self, combo_op: int) -> None:
        self.rb.pop()
        self.rb.append(weird_division(self.ra[0], self.combo_operand(combo_op)))
        self.instruction_pointer += 2

    def cdv(self, combo_op: int) -> None:
        self.rc.pop()
        self.rc.append(weird_division(self.ra[0], self.combo_operand(combo_op)))
        self.instruction_pointer += 2


def parse_program(path: Path) -> tuple[Computer, Program]:
    with open(path) as f:
        lines = f.read().splitlines()
    initial_registers = list(map(lambda line: int(line.split(":")[-1].strip()), lines[:3]))
    comp = Computer(initial_registers[0], initial_registers[1], initial_registers[2])
    program = list(map(lambda x: int(x), lines[-1].split(":")[-1].split(",")))
    return comp, program


def run_program(ra_start: int, comp: Computer, program: Program) -> list[int]:
    comp.ra = deque([ra_start])
    comp.instruction_pointer = 0
    output = []
    program_length = len(program)
    while True:
        if comp.instruction_pointer >= program_length:
            break
        result = comp.run_instruction(program[comp.instruction_pointer], program[comp.instruction_pointer + 1])
        if result is not None:
            output.append(result)
    return output


def iterate(comp: Computer, program: Program) -> None:
    for i in range(32):
        # if str(i)[0] != "3":
        #     continue
        guess = i
        output = run_program(guess, comp, program)

        # if output[-1] != 0:
        #     octal_convert = "".join(map(str, reversed(output)))
        # else:
        #     octal_convert = "".join(map(str, reversed(output[:-1]))) + str(output[-1])

        octal_convert = "".join(map(str, reversed(output)))
        if output[-1] == 0:
            check_octal = oct(i)
            results_dict = {
                "guess": guess,
                "check_octal": check_octal,
                "output": output,
                "octal_convert": octal_convert,
                "decimal_convert": int(octal_convert, 8),
            }
            print(results_dict)
            print(120 * "=")


async def brute_force(
    start: str, end_length: int, comp: Computer, program: Program, checked: set[int]
) -> list[int] | None:
    results_queue: Queue[tuple[int, list[int]]] = Queue(maxsize=20)
    for i in tqdm(
        itertools.product(*[range(0, 8) for _ in range(end_length)]), total=8**end_length, desc=f"{end_length}"
    ):
        end = "".join(map(str, i))
        test_value = int(start + end, 8)
        if test_value in checked:
            continue
        checked.add(test_value)
        if not results_queue.full():
            results_queue.put_nowait((test_value, run_program(test_value, comp, program)))
            continue
        real_val, output = await results_queue.get()
        if output == program:
            print(100 * "=")
            print(real_val)
            print(output)
            print(100 * "=")
            return output
    while not results_queue.empty():
        real_val, output = await results_queue.get()
        if output == program:
            print(100 * "=")
            print(real_val)
            print(output)
            print(100 * "=")
            return output
    return None


def main() -> None:
    comp, program = parse_program(Path("data/input17.txt"))
    print(run_program(comp.ra[0], comp, program))
    # Literally guess and checked working left to right. This is only off by the last (first) digit in the output but
    # we wound up having to back up 8 digits to find the solution
    start = "3045130136122400"
    checked: set[int] = set()
    for i in range(2, 16):
        result = asyncio.run(brute_force(start[:-i], i, comp, program, checked))
        if result is not None:
            return
    # The correct answer in octal
    correct_octal = "3045130145714775"
    print(run_program(int(correct_octal, 8), comp, program))


if __name__ == "__main__":
    main()

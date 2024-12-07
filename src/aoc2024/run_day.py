import argparse
import importlib
import time

import aoc2024


def main(day_number: str | None, time_execution: bool) -> None:
    day_list = [d for d in aoc2024.days]
    if not day_number:
        day = max(day_list)
    else:
        if len(day_number) == 1:
            day_number = f"0{day_number}"
        if f"day{day_number}" not in day_list:
            raise ValueError(f"Day does not exist. Available days:\n  {'\n  '.join(sorted(day_list))}")
        day = f"day{day_number}"
    print(f"Running: {day}")
    day_module = importlib.import_module(f"aoc2024.{day}.{day}")
    start = time.perf_counter()
    day_module.main()
    execution_time = time.perf_counter() - start
    if time_execution:
        print(f"exec time: {execution_time}")


def run() -> None:
    parser = argparse.ArgumentParser(description="AOC runner")
    parser.add_argument("-d", "--day", help="day to run, defaults to latest")
    parser.add_argument("-t", "--time", help="report execution time", action="store_true")
    args = parser.parse_args()
    main(args.day, args.time)


if __name__ == "__main__":
    run()

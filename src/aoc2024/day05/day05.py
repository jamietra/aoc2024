import functools
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable, Literal

RulesDict = defaultdict[int, list[int]]
Updates = list[list[int]]
ComparisonKeyFunction = Callable[[Any], Any]


def parse_rules(path: Path) -> tuple[RulesDict, Updates]:
    with open(path) as f:
        content = f.read()
    rules, updates = content.split("\n\n")
    rule_dict: RulesDict = defaultdict(list)
    for r in rules.split():
        first, after = map(int, r.split("|"))
        rule_dict[first].append(after)
    update_list = list(map(lambda line: list(map(int, line.split(","))), updates.split()))
    return rule_dict, update_list


def rule_comparison(a: int, b: int, rules: RulesDict) -> Literal[-1, 0, 1]:
    if a in rules[b]:
        return 1
    else:
        return -1


def get_key_function(rules: RulesDict) -> ComparisonKeyFunction:
    x = functools.cmp_to_key(functools.partial(rule_comparison, rules=rules))
    return x


def get_sorted_updates(updates: Updates, cmp_key_function: ComparisonKeyFunction) -> Updates:
    return [update for update in updates if sorted(update, key=cmp_key_function) == update]


def get_sorted_out_of_order(updates: Updates, cmp_key_function: ComparisonKeyFunction) -> Updates:
    return [sorted_update for update in updates if (sorted_update := sorted(update, key=cmp_key_function)) != update]


def get_middle_sum(updates: Updates) -> int:
    return sum([update[len(update) // 2] for update in updates])


def main() -> None:
    rules, updates = parse_rules(Path("data/input05.txt"))
    comp_key_function = get_key_function(rules)
    print(get_middle_sum(get_sorted_updates(updates, comp_key_function)))
    print(get_middle_sum(get_sorted_out_of_order(updates, comp_key_function)))


if __name__ == "__main__":
    main()

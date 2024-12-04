import functools
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable, Literal


def parse_rules(path: Path) -> tuple[defaultdict[int, list[int]], list[list[int]]]:
    with open(path) as f:
        content = f.read()
    rules, updates = content.split("\n\n")
    rule_dict: defaultdict[int, list[int]] = defaultdict(list)
    for r in rules.split():
        first, after = map(int, r.split("|"))
        rule_dict[first].append(after)
    update_list = list(map(lambda line: list(map(int, line.split(","))), updates.split()))
    return rule_dict, update_list


def rule_comparison(a: int, b: int, rules: defaultdict[int, list[int]]) -> Literal[-1, 0, 1]:
    if a in rules[b]:
        return 1
    else:
        return -1


def get_key_function(rules: defaultdict[int, list[int]]) -> Callable[[Any], Any]:
    x = functools.cmp_to_key(functools.partial(rule_comparison, rules=rules))
    return x


def main1(rules: defaultdict[int, list[int]], updates: list[list[int]]) -> None:
    """
    for posterity's sake my original approach to part one before passing the ordering to sort... This is much slower
    """
    in_order_updates = []
    out_of_order = []
    comp_key_function = get_key_function(rules)
    for update in updates:
        is_ordered = True
        reversed_update = list(reversed(update))
        for i, test_val in enumerate(reversed_update[:-1]):
            if rule_intesrection := set(rules[test_val]).intersection(set(reversed_update[(i + 1) :])):
                is_ordered = False
                probably_offending_number = list(rule_intesrection)[0]
                reversed_update[i] = probably_offending_number
                reversed_update[reversed_update.index(probably_offending_number)] = test_val
        if is_ordered:
            in_order_updates.append(update)
        else:
            out_of_order.append(sorted(update, key=comp_key_function))
    print(sum([x[len(x) // 2] for x in in_order_updates]))
    print(sum([x[len(x) // 2] for x in out_of_order]))


def main() -> None:
    rules, updates = parse_rules(Path("data/input05.txt"))
    comp_key_function = get_key_function(rules)
    in_order_updates = []
    out_of_order = []
    for update in updates:
        sorted_update = sorted(update, key=comp_key_function)
        if update == sorted_update:
            in_order_updates.append(update)
        else:
            out_of_order.append(sorted_update)
    print(sum([x[len(x) // 2] for x in in_order_updates]))
    print(sum([x[len(x) // 2] for x in out_of_order]))


if __name__ == "__main__":
    main()

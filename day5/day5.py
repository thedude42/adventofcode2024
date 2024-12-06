import sys
from collections import defaultdict
from math import floor


def reorder_invalid_update(update, order_index) -> list:
    has_rule = [ page in order_index for page in update ]
    i = len(update) - 1
    j = 0
    while i != j:
        while j != i:
            if has_rule[i] and update[j] in order_index[update[i]] and j < i:
                update[j], update[i] = (update[i], update[j])
                has_rule[j], has_rule[i] = has_rule[i], has_rule[j]
                j = 0
                continue
            j += 1
        j = 0
        i -= 1
    return update



def part2_entry(rules, updates):
    order_index = get_order_index(rules)
    updates_list = parse_updates_lines(updates)
    invalid_updates = [ update for update in updates_list if not is_valid_update(update, order_index) ]
    fixed_updates = [ reorder_invalid_update(update, order_index) for update in invalid_updates]
    print(f"Part 2: {sum([update[floor(len(update)/2)] for update in fixed_updates])}")


def get_order_index(rules: list) -> dict:
    return_index = defaultdict(set)
    for rule_line in rules:
        before, after = [ int(c) for c in rule_line.split('|')]
        return_index[before].add(after)
    return return_index


def parse_updates_lines(updates: list) -> list:
    return [ [ int(page) for page in line.split(',') ] for line in updates ]


def is_valid_update(update, order_index) -> bool:
    has_rule = [ page in order_index for page in update ]
    for i in range(len(update)-1, -1, -1):
        if has_rule[i]:
            for j in range(len(update)):
                if i != j:
                    if update[j] in order_index[update[i]] and j < i:
                        return False
    return True


def part1_entry(rules, updates):
    order_index = get_order_index(rules)
    updates_list = parse_updates_lines(updates)
    valid_updates = [ update for update in updates_list if is_valid_update(update, order_index) ]
    print(f"Part 1: {sum([update[floor(len(update)/2)] for update in valid_updates])}")



def main():
    if len(sys.argv) < 2:
        sys.exit("missing input")
    infile = sys.argv[1]
    lines = [ line for line in open(infile, 'r') ]
    divider = lines.index("\n")
    rules = lines[:divider]
    updates = lines[divider+1:]
    part1_entry(rules, updates)
    part2_entry(rules, updates)


if __name__ == '__main__':
    main()
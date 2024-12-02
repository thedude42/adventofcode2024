import sys


def search_bad_level(report: list) -> bool:
    for i in range(len(report)):
        if decide_safe([ n for idx, n in enumerate(report) if idx != i ]):
            return True
    return False


def part2_entry(input_filename):
    with open(input_filename, 'r') as report_file:
        safe_count = 0
        reports = [ [ int(n) for n in l.split() ] for l in report_file ]
        for report in reports:
            if decide_safe(report):
                safe_count += 1
            else:
                if search_bad_level(report):
                    safe_count += 1
        print(f"part 2: {safe_count}")


def decide_safe(report: list) -> bool:
    last_change = None
    for x in range(1, len(report)):
        change = report[x] - report[x-1]
        if abs(change) > 3:
                return False
        elif change == 0:
            return False
        if last_change is not None:
            if (change < 0 and last_change > 0) or (change > 0 and last_change < 0):
                return False
        last_change = change
    return True


def part1_entry(input_filename):
    with open(input_filename, 'r') as report_file:
        reports = [ [ int(n) for n in l.split() ] for l in report_file ]
        safe_status = [ decide_safe(report) for report in reports ]
        # print(reports)
        # print(safe_status)
        print(f"part 1: {safe_status.count(True)}")


def main():
    if len(sys.argv) < 2:
        sys.exit("missing input")
    infile = sys.argv[1]
    part1_entry(infile)
    part2_entry(infile)


if __name__ == '__main__':
    main()
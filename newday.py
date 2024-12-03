import sys


def part2_entry(input_filename):
    pass


def part1_entry(input_filename):
    pass


def main():
    if len(sys.argv) < 2:
        sys.exit("missing input")
    infile = sys.argv[1]
    part1_entry(infile)
    part2_entry(infile)


if __name__ == '__main__':
    main()
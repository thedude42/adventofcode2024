import sys


def num_found(anum, search_list):
    found = 0
    for x in search_list:
        if anum == x:
            found += 1
    return found

def part2_entry(input_filename):
    with open(input_filename, 'r') as infile:
        tup_list = [ (int(l[0].strip()), int(l[1].strip())) for l in [ l.split() for l in infile.readlines() ] ]
        left = sorted([ t[0] for t in tup_list ])
        right = sorted([ t[1] for t in tup_list ])
        similarity_scores = []
        for lnum in left:
            similarity_scores.append(lnum * num_found(lnum, right))
        print(f"part2: {sum(similarity_scores)}")

def part1_entry(input_filename):
    with open(input_filename, 'r') as infile:
        tup_list = [ (int(l[0].strip()), int(l[1].strip())) for l in [ l.split() for l in infile.readlines() ] ]
        left = sorted([ t[0] for t in tup_list ])
        right = sorted([ t[1] for t in tup_list ])
        differences = []
        for pair in zip(left, right):
            differences.append(abs(pair[0] - pair[1]))
        print(f"part1: {sum(differences)}")



def main():
    if len(sys.argv) < 2:
        sys.exit("missing input")
    infile = sys.argv[1]
    part1_entry(infile)
    part2_entry(infile)


if __name__ == '__main__':
    main()
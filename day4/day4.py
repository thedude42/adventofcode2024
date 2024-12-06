import sys
from collections import defaultdict
from functools import reduce


class WordMatrix:

    def __init__(self, matrix) -> None:
        assert type(matrix) == list
        self.matrix = matrix
        self.__charmap = None
    

    @property
    def char_map(self):
        if self.__charmap is None:
            charmap = defaultdict(list)
            for x in range(len(self.matrix)):
                for y in range(len(self.matrix[0])):
                    charmap[self.matrix[x][y]].append((x,y))
            self.__charmap = charmap
        return self.__charmap


    def get_xmas_horrizontal_strings(self, start):
        assert self.matrix[start[0]][start[1]] == 'X'
        xmas_count = 0
        if start[1] <= len(self.matrix[0]) - 4:
            if ''.join([self.matrix[start[0]][start[1]+n] for n in range(4)]) == 'XMAS':
                xmas_count += 1
        if start[1] >= 3:
            if ''.join([self.matrix[start[0]][start[1]-n] for n in range(4)]) == 'XMAS':
                xmas_count += 1
        if xmas_count > 0:
            print(f"{xmas_count} horrizontal from {start}")
        return xmas_count
    

    def get_xmas_vertical_strings(self, start):
        assert self.matrix[start[0]][start[1]] == 'X'
        xmas_count = 0
        if start[0] <= len(self.matrix) - 4:
            down = ''.join([self.matrix[start[0]+n][start[1]] for n in range(4)])
            if down == 'XMAS':
                xmas_count += 1
        if start[0] >=  3:
            up = ''.join([self.matrix[start[0]-n][start[1]] for n in range(4)])
            if up == 'XMAS':
                xmas_count += 1
        if xmas_count > 0:
            print(f"{xmas_count} vertical from {start}")
        return xmas_count
    

    def get_xmas_diag_strings(self, start, target_string='XMAS', return_type='count'):
        assert self.matrix[start[0]][start[1]] == target_string[0]
        xmas_count = 0
        match_coords = []
        # diag-down-right
        if start[0] <= len(self.matrix) - len(target_string) and start[1] <= len(self.matrix[0]) - len(target_string):
            down_right = ''.join([self.matrix[start[0]+n][start[1]+n] for n in range(len(target_string))])
            #print(down_right)
            if down_right == target_string:
                match_coords.append([(start[0]+n, start[1]+n) for n in range(len(target_string))])
                xmas_count += 1
        # diag-down-left
        if start[0] <= len(self.matrix) - len(target_string) and start[1] >= len(target_string)-1:
            down_left = ''.join([self.matrix[start[0]+n][start[1]-n] for n in range(len(target_string))])
            #print(down_left)
            if down_left == target_string:
                match_coords.append([(start[0]+n, start[1]-n) for n in range(len(target_string))])
                xmas_count += 1
        # diag-up-right
        if start[0] >= len(target_string)-1 and start[1] <= len(self.matrix[0]) - len(target_string):
            up_right = ''.join([self.matrix[start[0]-n][start[1]+n] for n in range(len(target_string))])
            #print(up_right)
            if up_right == target_string:
                match_coords.append([(start[0]-n, start[1]+n) for n in range(len(target_string))])
                xmas_count += 1
        #diag-up-left
        if start[0] >= len(target_string)-1 and start[1] >= len(target_string)-1:
            up_left = ''.join([self.matrix[start[0]-n][start[1]-n] for n in range(len(target_string))])
            #print(up_left)
            if up_left == target_string:
                match_coords.append([(start[0]-n, start[1]-n) for n in range(len(target_string))])
                xmas_count += 1
        assert len(match_coords) == xmas_count
        if return_type != 'count':
            return match_coords
        return xmas_count
        
    
    def find_linear_xmas(self):
        total = 0
        for start in self.char_map['X']:
            print(f"looking: {start}")
            total += self.get_xmas_horrizontal_strings(start)
            total += self.get_xmas_vertical_strings(start)
            total += self.get_xmas_diag_strings(start)
        return total
    
    # For reference, my original pathfinding algorithm when I misunderstood part 1
    #
    #
    # def get_neighbors(self, coords_tuple):
    # print(f"coords_tuple: {coords_tuple}")
    # neighbors = set()
    # for x in range(coords_tuple[0] - 1, coords_tuple[0] + 2):
    #     if x < 0:
    #         continue
    #     elif x >= len(self.matrix):
    #         continue
    #     for y in range(coords_tuple[1] - 1, coords_tuple[1] + 2):
    #         if y < 0:
    #             continue
    #         elif y >= len(self.matrix[0]):
    #             continue
    #         neighbors.add(((x,y)))
    # return neighbors


    # def find_xmas(self):
    #     #print(self.char_map)
    #     path_stack = [ [coord] for coord in self.char_map['X']]
    #     xmas = 'XMAS'
    #     xmas_count = 0
    #     while len(path_stack) > 0 and xmas_count <= 18:
    #         print(f"path_stack: {path_stack}")
    #         current = path_stack.pop(0)
    #         if len(current) == len(xmas):
    #             assert ''.join([self.matrix[tup[0]][tup[1]] for tup in current]) == xmas
    #             xmas_count += 1
    #             continue
    #         neighbors = self.get_neighbors(current[-1])
    #         #print(f"neighbors: {neighbors}")
    #         #print(f"{xmas[len(current)]} coords: {self.char_map[xmas[len(current)]]}")
    #         neighbor_matches = [ coord for coord in self.char_map[xmas[len(current)]] if coord in neighbors]
    #         #print(f"{neighbor_matches}")
    #         for next_coord in neighbor_matches:
    #             #print(f"current: {current} | next_coord: {next_coord}")
    #             next_path = current.copy()
    #             next_path.append(next_coord)
    #             if next_path not in path_stack:
    #                 path_stack.append(next_path)
    #     print(xmas_count)
            


def part2_entry(input_filename):
    wordsearch = [ line.strip() for line in open(input_filename, 'r') ]
    m = WordMatrix(wordsearch)
    diag_mases = []
    for start in m.char_map['M']:
        diag_mases += m.get_xmas_diag_strings(start, target_string='MAS', return_type='coord_list')
    i = 0
    j = 1
    x_mas_count = 0
    while len(diag_mases) > 1:
        assert len(diag_mases[i]) == 3
        assert len(diag_mases[j]) == 3
        if diag_mases[i][1] == diag_mases[j][1]:
            x_mas_count += 1
            diag_mases.pop(j)
            diag_mases.pop(i)
            i = 0
            j = 1
            continue
        else:
            j += 1
        if j >= len(diag_mases):
            diag_mases.pop(0)
            i = 0
            j = 1
    print(f"Part 2: {x_mas_count}")
    

def part1_entry(input_filename):
    wordsearch = [ line.strip() for line in open(input_filename, 'r') ]
    m = WordMatrix(wordsearch)
    print(f"Part 1: {m.find_linear_xmas()}")


def main():
    if len(sys.argv) < 2:
        sys.exit("missing input")
    infile = sys.argv[1]
    part1_entry(infile)
    part2_entry(infile)


if __name__ == '__main__':
    main()
import sys


class MulInstruction:

    def __init__(self, param1, param2) -> None:
        assert type(param1) == type(param2) == int
        self.param1 = param1
        self.param2 = param2
    

    def __call__(self):
        return self.param1 * self.param2

class MulParser:

    CHARTOKS = ['m', 'u', 'l', '(', ')', ',', 'd', 'o', 'n', '\'', 't']
    MUL = CHARTOKS[:3]
    CONTROL = CHARTOKS[6:]
    PARENS = CHARTOKS[3:5]


    def __init__(self, memory_file: str, stateful=False) -> None:
        self.memory_file = memory_file
        self.stateful = stateful
        self.enabled = True
        self.__reset()

    
    def __call__(self):
        with open(self.memory_file, 'r') as memfile:
            for line in memfile:
                for character in line:
                    #print(self.buffer, character, self.control_buffer)
                    if character not in MulParser.CHARTOKS and not character.isnumeric():
                        self.__reset()
                    elif character in MulParser.CONTROL:
                        if self.stateful:
                            self.parse_control_word(character)
                        else:
                            self.__reset()
                    elif not self.enabled and character in MulParser.PARENS and self.parsing_control:
                        if character == '(':
                            self.parse_lparen(character)
                        else:
                            self.parse_rparen(character)
                    elif self.enabled:
                        if character in MulParser.MUL:
                            self.parse_mul(character)
                        elif character == '(':
                            self.parse_lparen(character)
                        elif character.isnumeric():
                            self.parse_numeric(character)
                        elif character == ',':
                            self.parse_comma(character)
                        elif character == ')':
                            if self.parse_rparen(character):
                                if self.first_param is not None and self.second_param is not None:
                                    if not self.stateful or self.enabled:
                                        yield MulInstruction(self.first_param, self.second_param)
                                    else:
                                        yield
                                    self.__reset()
                    else:
                        assert not self.enabled

    

    @property
    def parsing_mul(self):
        if ''.join(self.buffer).startswith('mul('):
            return 'COMPLETE'
        elif len(self.buffer) > 0:
            return True
    

    @property
    def parsing_control(self):
        return bool(len(self.control_buffer))
    

    @property
    def parsing(self):
        assert len(self.buffer) == 0 or len(self.control_buffer) == 0
        if self.stateful:
            return self.parsing_control or self.parsing_mul
        else:
            return self.parsing_mul
    

    def parse_mul(self, ch):
        assert ch in 'mul'
        if len(self.buffer) > 3:
            self.__reset()
            return False
        elif not self.parsing and ch == 'm':
            self.buffer.append(ch)
        elif len(self.buffer) == 1 and ch == 'u':
            self.buffer.append(ch)
        elif len(self.buffer) == 2 and ch == 'l':
            self.buffer.append(ch)
        else:
            self.__reset()
            return False
        return True
    

    def parse_control_word(self, ch):
        assert ch in "don't"
        if self.parsing_mul:
            self.__reset()
            return False
        elif not self.parsing and ch == 'd':
            self.control_buffer.append(ch)
        elif len(self.control_buffer) >= 5:
            self.__reset()
            return False
        elif self.parsing_control:
            if len(self.control_buffer) == 1 and ch == 'o':
                self.control_buffer.append(ch)
            elif len(self.control_buffer) == 2 and ch == 'n':
                self.control_buffer.append(ch)
            elif len(self.control_buffer) == 3 and ch == '\'':
                self.control_buffer.append(ch)
            elif len(self.control_buffer) == 4 and ch == 't':
                self.control_buffer.append(ch)
        else:
            self.__reset()
            return False
        return True

    def parse_lparen(self, ch):
        assert ch == '('
        if not self.parsing:
            self.__reset()
            return False
        if self.parsing_mul and len(self.buffer) == 3:
            self.buffer.append(ch)
        elif self.stateful and self.parsing_control:
            if len(self.control_buffer) == 2:
                self.control_buffer.append(ch)
            elif len(self.control_buffer) == 5:
                self.control_buffer.append(ch)
            else:
                self.__reset()
                return False
        else:
            self.__reset()
            return False
        return True
    

    def parse_numeric(self, ch):
        assert ch.isnumeric()
        if self.parsing_mul == 'COMPLETE' and self.buffer[-1] in '(,1234567890':
            self.buffer.append(ch)
        else:
            self.__reset()
            return False
        return True
    

    def parse_comma(self, ch):
        assert ch == ','
        if self.first_param is None and self.parsing_mul == 'COMPLETE':
            param_start = self.buffer.index('(') + 1
            self.first_param = int(''.join(self.buffer[param_start:]))
            self.buffer.append(ch)
        else:
            self.__reset()
            return False
        return True
    

    def parse_rparen(self, ch):
        assert ch == ')'
        if not self.parsing:
            self.__reset()
            return False
        elif self.stateful and self.parsing_control:
            if ''.join(self.control_buffer) == 'do(':
                self.__enable()
                self.__reset()
            elif ''.join(self.control_buffer) == "don't(":
                self.__disable()
                self.__reset()
            else:
                self.__reset()
                return False
        elif not self.parsing_mul == 'COMPLETE' or self.first_param is None:
            self.__reset()
            return False
        elif self.first_param is not None:
            param_start = self.buffer.index(',') + 1
            self.second_param = int(''.join(self.buffer[param_start:]))
            # CAN'T RESET YET!
        else:
            self.__reset()
            return False
        return True


    def __enable(self):
        self.enabled = True
    

    def __disable(self):
        self.enabled = False


    def __reset(self):
        self.first_param = None
        self.second_param = None
        self.buffer = []
        self.control_buffer = []


def part2_entry(input_filename):
    parser = MulParser(input_filename, True)
    print(f"Part 2: {sum([ instruction() for instruction in parser() if instruction is not None])}")

def part1_entry(input_filename):
    parser = MulParser(input_filename)
    print(f"Part 1: {sum([ instruction() for instruction in parser() if instruction is not None])}")


def main():
    if len(sys.argv) < 2:
        sys.exit("missing input")
    infile = sys.argv[1]
    part1_entry(infile)
    part2_entry(infile)


if __name__ == '__main__':
    main()
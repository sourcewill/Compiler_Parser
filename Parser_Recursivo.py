
input_file = 'input.txt'
current_pointer = -1
current_symbol = ''
current_line = ''

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
extended_alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_']

operators = ['+', '-', '*', "/", '^']

reserved_words = ['print']

def read_input_file():

    global input_file

    file = open(input_file, 'r')
    lines = file.readlines()
    ret = []
    # Remove espacos e quebra de linhas
    for line in lines:
        line = line.replace(' ', '').replace('\n', '')
        ret.append(line)
    file.close()
    return ret


def next_symbol():

    global current_pointer, current_line, current_symbol

    current_pointer += 1
    if current_pointer >= len(current_line):
        current_symbol = '$'
        return
    current_symbol = current_line[current_pointer]


def restore_pointer(backup_pointer):

    global current_pointer, current_line, current_symbol

    current_pointer = backup_pointer
    if current_pointer >= len(current_line):
        current_symbol = '$'
        return
    current_symbol = current_line[backup_pointer]


def reserved_word(word):

    global current_pointer, current_symbol

    backup_pointer = current_pointer

    for letter in word:
        if current_symbol == letter:
            next_symbol()
        else:
            restore_pointer(backup_pointer)
            return False
                    
    return True


# N  -> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0N | 1N | 2N | 3N | 4N | 5N | 6N | 7N | 8N | 9N
def N():

    global current_pointer, current_symbol

    for num in numbers:
        if current_symbol == num:
            next_symbol()
            backup_pointer = current_pointer        
            if N():
                return True
            restore_pointer(backup_pointer)
            return True

    return False


# F -> N,N
def F():

    global current_pointer, current_symbol

    backup_pointer = current_pointer

    if N():
        if current_symbol == ',':
            next_symbol()
            if N():
                return True

    restore_pointer(backup_pointer)
    return False


# I  -> "a"I2 | "b"I2 | "c"I2 | ... | "A"I2 | "B"I2 | "C"I2 | ...
def I():

    global current_pointer, current_symbol

    backup_pointer = current_pointer 

    # Checks if it is not a reserved word
    for word in reserved_words:
        if reserved_word(word):
            restore_pointer(backup_pointer)
            return False;

    restore_pointer(backup_pointer)

    for letter in alphabet:
        if current_symbol == letter:
            next_symbol()
            backup_pointer = current_pointer        
            if I2():
                return True
            restore_pointer(backup_pointer)
            return True

    return False

# I2  -> "a"I2 | "b"I2 | "c"I2 | ... | "A"I2 | "B"I2 | "C"I2 | ... | "0"I2 | "1"I2 | "2"I2 | ... | "_"I2
def I2():

    global current_pointer, current_symbol

    backup_pointer = current_pointer 

    for letter in extended_alphabet:
        if current_symbol == letter:
            next_symbol()
            backup_pointer = current_pointer        
            if I2():
                return True
            restore_pointer(backup_pointer)
            return True

    return False


# E  -> NE' | FE' | IE' | (E)E'
def E():

    global current_pointer, current_symbol

    backup_pointer = current_pointer

    if N():
        if current_symbol != ',':
            if E2():
                return True

    restore_pointer(backup_pointer)

    if F():
        if E2():
            return True

    restore_pointer(backup_pointer)

    if I():
        if E2():
            return True

    restore_pointer(backup_pointer)

    if current_symbol == '(':
        next_symbol()
        if E():
            if current_symbol == ')':
                next_symbol()
                if E2():
                    return True

    restore_pointer(backup_pointer)

    return False


# E' -> +EE' | -EE' | *EE' | /EE' | ^EE' | vazio
def E2():

    global current_pointer, current_symbol

    backup_pointer = current_pointer

    for op in operators:        
        if current_symbol == op:
            next_symbol()
            if E():
                if E2():
                    return True
            restore_pointer(backup_pointer)

    return True


# S -> E | "print"E | I=E
def S():

    global current_pointer, current_symbol

    backup_pointer = current_pointer

    if E():
        if current_symbol != '=': # There cannot be an assignment after an expression.
            return True

    restore_pointer(backup_pointer)

    if reserved_word('print'):
        if E():
            return True

    restore_pointer(backup_pointer)

    if I():
        if current_symbol == '=':
            next_symbol()
            if E():
                return True

    restore_pointer(backup_pointer)
    return False


def main():

    global current_pointer, current_line, current_symbol

    for line in read_input_file():

        current_line = line

        if line == '':
            continue

        current_pointer = -1                
        next_symbol()

        print('Line: ' + current_line)
        
        if S():
            if current_symbol == '$':
                print('Valid line.\n')
                continue
        print('Invalid line! pointer -> ' + current_symbol + '\n')


main()
#import board
#import pulseio
# from analogio import AnalogIn
#from digitalio import DigitalInOut, Direction, Pull
# import time
# import random

import joyish_tests as testing
    
# Digital input with pullup
#red = DigitalInOut(board.D13)
#red.direction = Direction.OUTPUT
#green = DigitalInOut(board.D2)
#green.direction = Direction.OUTPUT

# ToDo: make lamda notation
#       make parser for easy input (trivial to split on spaces)
#       ui/repl

def _dup(s, pl):
    a = s.pop()
    s.append(a)
    s.append(a)
    return [s, pl]
def _add(s, pl):
    a = s.pop()
    b = s.pop()
    s.append(a + b)
    return [s, pl]
def _sub(s, pl):
    a = s.pop()
    b = s.pop()
    s.append(b - a)
    return [s, pl]
def _prod(s, pl):
    a = s.pop()
    b = s.pop()
    s.append(a * b)
    return [s, pl]
def _n_prod(s, pl):
    if len(s) >= 2:
        a = s.pop()
        b = s.pop()
        if isNumber(a) and isNumber(b):
            s.append(a * b)
            pl.insert(0, 'n*')
            return [s, pl]
        else:
            s.append(b)
            s.append(a)
    return [s, pl];
def _eq(s, pl):
    a = s.pop()
    b = s.pop()
    s.append(a == b)
    return [s, pl]
def _ift(s, pl):
    then_block = s.pop()
    expression = s.pop()
    if expression:
        if isArray(then_block):
            pl = then_block+pl
        else:
            pl.insert(0, then_block)
    return [s, pl]
def _ifte (s, pl):
    else_block = s.pop()
    then_block = s.pop()
    expression = s.pop()
    if expression:
        if isArray(then_block):
            print(then_block)
            pl = then_block+pl
        else:
            pl.insert(0, then_block)
    else:
        if isArray(else_block):
            pl = else_block+pl
        else:
            pl.insert(0, else_block)
    return [s, pl]
def _openList (s, pl):
    thelist = []
    next = pl[0];
    pl = pl[1:]
    nesting = 0
    while ((len(pl) > 0 and next != ']') or nesting > 0):
        thelist.append(next)
        if next == '[':
            nesting += 1
        if next == ']':
            nesting -= 1
        next = pl[0];
        pl = pl[1:]

    pl.insert(0, thelist)
    return [s, pl]


words = {
  'dup': _dup,
  '+': _add,
  '-': _sub,
  '*': _prod,
  'n*': _n_prod,
  '==': _eq,
  'if': _ift,
  'if-else': _ifte,
  '[': _openList,
  'count-down': 'dup 1 - [ dup 1 - count-down ] if',
  'fact': 'count-down n*'
}
#program_list = '9 7 + 2.5 *'
#program_list = '9 7 2.4 +'
#program_list = '9 7 swap'
#program_list = '1 2 3 dup'
#program_list = '1 2 3 dup2'
#program_list = '9 7 swap dup'
#program_list = '1 4 fact'
#program_list = '4 count-down'
#program_list = '1 4 count-up'
#program_list = '1 >R noop <R 1 assert'
#program_list = '5 >Q noop Q> 5 assert'
#program_list = '7 9 7 9 2 assert-n'
#program_list = '1 2 5 2 n>R <R <R'
#program_list = '1 2 5 >Q >Q Q> Q>'
#program_list = '1 3 5 2 n>Q Q> Q> 3 assert 5 assert 1 assert'
#program_list = '1 3 5 8 3 n>Q Q> Q> Q> 3 assert 5 assert 8 assert 1 assert'
#program_list = ' 4 yes if-then 1 yes if-then 0 no yes if-then-else -1 yes if-then'
#program_list = '0 0 1 if-then-else 1 not'
#program_list = '1 inverse 1.0 inverse -3 inverse -1.02 inverse'
#program_list = '1 0 1 1--inverse if-then-else'
#program_list = '1 redLED 1 greenLED'
#program_list = '1 redLED 1.5 0 1--redLED timeOut'
#program_list = ' 1 redLED 1 0 1--redLED if-then 1 1 1--redLED if-then'
#program_list = ' 0 redLED 1 1 1--redLED if-then'
#program_list = ' 1 0 1--redLED 1 1--redLED if-then-else'
#program_list = '4 count-down * * *'

# recursive example
# 4 fact
# 1 2 * 3 * 4 *
# :fact dup 1 * swap -1 + swap fact;
param_stack = []
return_stack = []
return_queue = []
assertions = []

def isTrue(e):
    if e != 0 and e != False and e != 'False':
        return True
    return False

def isValue(e, fun):
    return (isinstance(e, int) or isinstance(e, float)
            or (isinstance(e, str) and not e in fun.keys()))

def isNumber(e):
    return isinstance(e, int) or isinstance(e, float)

def isArray(a):
    return isinstance(a, (list,))

#from inspect import isfunction
def isfunction(candidate):
    return not (isinstance(candidate, str) or isinstance(candidate, (list,)))

def number_or_str(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            if s == 'True':
                return 'True'
            if s == 'False':
                return 'False'
            return s

def cmpLists(a, b):
    same = True
    if len(a) == len(b):
        for i in range(len(a)):
            if a[i] != b[i]:
                same = False
    else:
        same = False
    return same

def joinStrings(pl):
    new_pl = []
    terminal_char = ''
    new_string = ''
    for i in range(len(pl)):
        word = pl[i]
        if isinstance(word, str) and len(word) > 0:
            if word[0] == '"' and terminal_char == '':
                print('enter "string"')
                new_string += word[1:]
                terminal_char = '"'
            elif word[0] == "'" and terminal_char == "":
                print("enter 'string'")
                new_string += word[1:]
                terminal_char = "'"
            elif word[len(word)-1] == '"' and terminal_char == '"':
                new_string += ' ' + word[:-1]
                terminal_char = ''
            elif word[len(word)-1] == "'" and terminal_char == "'":
                new_string += ' ' + word[:-1]
                terminal_char = ""
            elif terminal_char != '':
                new_string += ' ' + word
        elif terminal_char != '':
            new_string += ' ' + str(word)
                
        if terminal_char == '' and new_string != '':
            new_pl.append(new_string)
            new_string = ''
        elif terminal_char == '':
            new_pl.append(word)
    
    return new_pl

def run(program_list, vs, fun):
    global assertions
    rs = []
    q = []
    pl = [ number_or_str(x) for x in program_list.split()]
    pl = joinStrings(pl)
    print(program_list)
    while len(pl) > 0: # and not isValue(pl[-1]):
        next = pl[0];
        pl = pl[1:]
        #print(vs, next, 'R:', rs, 'Q:', q)
        if isValue(next, fun) or isArray(next):
            vs.append(next)
            continue
        
        if next in fun.keys():
            print(vs, next, pl)
            if isfunction(fun[next]):
                (vs, pl) = fun[next](vs, pl)
            else:
                next_list = [ number_or_str(x) for x in fun[next].split()]
                pl = next_list + pl
            continue
    return vs


print('so far so good... ready to:')
#run(program_list, param_stack, fundi)
#print(param_stack, 'Assertions:', assertions)

# tests
print('Starting tests:')
for test in testing.tests:
    pl = test[0]
    param_stack = []
    expected_stack = test[1]
    result_stack = run(pl, param_stack, words)
    if not cmpLists(result_stack, expected_stack):
        print(param_stack, ' expected:', expected_stack)
        print('---- Failed test for: ', pl)



#while True: #loop forever
#    rs = read_rotor()
#    if rs == 1 or rs == -1:
#        stack.append(str(rs))
#        stack.append('rotary')
#        run(stack, fun)
    

#import board
#import pulseio
# from analogio import AnalogIn
#from digitalio import DigitalInOut, Direction, Pull
# import time
# import random

import forthup_tests as tests

# Digital input with pullup
#red = DigitalInOut(board.D13)
#red.direction = Direction.OUTPUT
#green = DigitalInOut(board.D2)
#green.direction = Direction.OUTPUT

# ToDo: make lamda notation
#       make parser for easy input (trivial to split on spaces)
#       ui/repl

fundi = {'rotary': '0--green 0--red if-then-else',
       'abs': '0 < 0--inverse if-then',
       'inverse': '-1 *',
       'not': '0 1 if-then-else',
       'noop': '',
       'red': '.abs redLED',
       'green': '.abs greenLED',
       'redLED': '',
       'greenLED': '',
       'dup2': '',
       'fact': 'dup 0--fact_aux if-then',
       'fact_aux': 'dup2 * swap -1 + swap fact',
       'count-down': 'dup -1 + 0--count-down_aux if-then',
       'count-down_aux': 'dup -1 + count-down',
       'count-up': 'dup2 inverse + 0--count-up_aux 0--drop if-then-else',
       'count-up_aux': '>R dup 1 + <R count-up',
       '+': '',
       '-': '',
       '*': '',
       '/': '',
       '%': '',
       'A&': '',
       'repeat': '',
       'assert': '= True 1-->A False 1-->A if-then-else',
       'assert-n': 'dup >R n>Q assert-n-2',
       'assert-n-2': 'dup >R 0--assert-n_aux if-then <R -1 +',
       'assert-n_aux': 'Q> assert <R -1 +  assert-n-2',
       'x_assert-n-unload': 'dup >R 0--assert if-then <R drop',
       'if-then': '',
       'if-then-else': '',
       'timeOut': '',
       'dup': '',
       'swap': '',
       'drop': '',
       '=': '',
       '>': '',
       '<': '',
       '>R': '',
       '>A': '',
       'n>R': 'dup', '>Q': '0--n>R_aux if-then', 'n>R_aux': '>R Q> -1 + n>R', '<R': '', 'n<R': '',
       '>Q': '',
       'n>Q': 'dup >R 0--n>Q_aux if-then',
       'n>Q_aux': '>Q <R -1 + n>Q',
       'Q>': ''}
#facts = {}
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
program_list = '4 count-down * * *'

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

def run(program_list, vs, fun):
    global assertions
    rs = []
    q = []
    pl = [ number_or_str(x) for x in program_list.split()]
    print(program_list)
    while len(pl) > 0: # and not isValue(pl[-1]):
        next = pl[0];
        pl = pl[1:]
        #print(vs, next, 'R:', rs, 'Q:', q)
        if isValue(next, fun):
            vs.append(next)
            continue
            
        if next == 'if-then':
            then_block = vs.pop()
            (then_args, then_block) = getArgs(then_block, vs)
                
#            if len(vs) >= 1:
            exp = vs.pop()
#                print('stack exp', exp)
#            else:
#                print('stack empty')
#                exp = False
            if isTrue(exp):
                #print('if clause is True')
                vs.extend(then_args)
                if isinstance(then_block, list):
                    pl = then_block.extend(pl)
                else:
                    pl.insert(0, then_block)
            continue
            
        if next == 'if-then-else':
            else_block = vs.pop()
            (else_args, else_block) = getArgs(else_block, vs)

            then_block = vs.pop()
            (then_args, then_block) = getArgs(then_block, vs)

#            if len(vs) >= 1:
            exp = vs.pop()
#            else:
#                print('stack empty')
#                exp = False
            if isTrue(exp):
                #print('if clause is True')
                vs.extend(then_args)
                if isinstance(then_block, list):
                    pl = then_block.extend(pl)
                else:
                    pl.insert(0, then_block)
            else:
                #print('if clause is False')
                vs.extend(else_args)
                if isinstance(else_block, list):
                    pl = else_block.extend(pl)
                else:
                    pl.insert(0, else_block)
            continue
            
        if next == '=':
            v1 = vs.pop()
            v2 = vs.pop()
            vs.append(v1 == v2)
            continue
            
        if next == '>':
            v1 = vs.pop()
            v2 = vs.pop()
            vs.append(v1 > v2)
            continue
            
        if next == '<':
            v1 = vs.pop()
            v2 = vs.pop()
            vs.append(v1 < v2)
            continue
            
        if next == '>A':
            v = vs.pop()
            assertions.append(v)
            continue
            
        if next == '>R':
            v = vs.pop()
            rs.append(v)
            continue
            
        if next == '<R':
            v = rs.pop()
            vs.append(v)
            continue
            
        if next == '>Q':
            v = vs.pop()
            q.insert(0, v)
            continue
            
        if next == 'Q>':
            v = q.pop()
            vs.append(v)
            continue
            
        if next == 'dup':
            vs.append(vs[-1])
            continue
            
        if next == 'dup2':
            vs.append(vs[-2])
            vs.append(vs[-2])
            continue
            
        if next == 'swap':
            lhs = vs.pop()
            rhs = vs.pop()
            vs.append(lhs)
            vs.append(rhs)
            continue
            
        if next == 'drop':
            vs.pop()
            continue
            
        if next == '+':
#            if len(vs) < 2:
#                print('Error: function '++ next ++ ' has insufficient arguments.')
#                break
            lhs = vs.pop()
            rhs = vs.pop()
            vs.append(lhs + rhs)
            continue
            
        if next == '-':
#            if len(vs) < 2:
#                print('Error: function '++ next ++ ' has insufficient arguments.')
#                break
            lhs = vs.pop()
            rhs = vs.pop()
            vs.append(lhs - rhs)
            continue
            
        if next == '*':
#            if len(vs) < 2:
#                print('Error: function '++ next ++ ' has insufficient arguments.')
#                break
            lhs = vs.pop()
            rhs = vs.pop()
            vs.append(lhs * rhs)
            continue
            
        if next == 'A&':
#            if len(vs) < 2:
#                print('Error: function '++ next ++ ' has insufficient arguments.')
#                break
            lhs = bool(assertions.pop())
            rhs = bool(assertions.pop())
            assertions.append(lhs and rhs)
            continue
            
#        if next == '/':
#            if len(vs) < 2:
#                print('Error: function '++ next ++ ' has insufficient arguments.')
#                break
#            lhs = vs.pop()
#            rhs = vs.pop()
#            vs.append(lhs / rhs)
#            continue
#
#        if next == '%':
#            if len(vs) < 2:
#                print('Error: function '++ next ++ ' has insufficient arguments.')
#                break
#            lhs = vs.pop()
#            rhs = vs.pop()
#            vs.append(lhs % rhs)
#            continue
            
#        if next == 'redLED':
#            val = vs.pop()
#            red.value = isTrue(val)
#            continue
            
#        if next == 'greenLED':
#            val = vs.pop()
#            green.value = isTrue(val)
#            continue
            
        if next in fun.keys():
            #print(vs, next, 'R:', rs, 'Q:', q)
            next_list = [ number_or_str(x) for x in fun[next].split()]
            pl = next_list + pl
            continue


def getArgs(block, vs):
    args = []
    if isinstance(block, str) and block[1:3] == '--':
        # eg. 3--my-fn will consume 3 arguments and the name of the function is 'my-fn'
        arity = int(block[:1])
        block = block[3:]
        #print('block', block)
        for i in range(0, arity):
            args.append(vs.pop())
    #print('args', args, 'block', block )
    return (args, block)
    
print('so far so good... ready to:')
#run(program_list, param_stack, fundi)
#print(param_stack, 'Assertions:', assertions)

# tests
print('  test')
for pl in tests.test_suite:
    param_stack = []
    assertions = []
    run(pl, param_stack, fundi)
    if assertions[0] != 'True' and assertions[0] != True:
        print(param_stack, 'Assertions:', assertions)
        print('---- Failed test for: ', pl)



#while True: #loop forever
#    rs = read_rotor()
#    if rs == 1 or rs == -1:
#        stack.append(str(rs))
#        stack.append('rotary')
#        run(stack, fun)
    

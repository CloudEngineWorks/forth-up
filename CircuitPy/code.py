import board
#import pulseio
# from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
import time
# import random
# Digital input with pullup
red = DigitalInOut(board.D13)
red.direction = Direction.OUTPUT
#green = DigitalInOut(board.D2)
#green.direction = Direction.OUTPUT

# ToDo: make lamda notation
#       make parser for easy input (trivial to split on spaces)
#       ui/repl

fundi = {'rotary':['0--green', '0--red', 'if-then-else'],
       'abs': ['0--noop', '0--inverse', 'if-then'],
       'inverse': [-1, '*'],
       'not': [0, 1, 'if-then-else'],
       'noop': [],
       'red': ['.abs', 'redLED'],
       'green': ['.abs', 'greenLED'],
       'redLED': [],
       'greenLED': [],
       'dup2': [],
       'fact': ['dup', '0--fact_aux', 'if-then'],
       'fact_aux': ['dup2', '*', 'swap', -1, '+', 'swap', 'fact'],
       'count-down': ['dup', -1, '+', '0--count-down_aux', 'if-then'],
       'count-down_aux': ['dup', -1, '+', 'count-down'],
       'count-up': ['dup2', 'inverse', '+', '0--count-up_aux', '0--drop', 'if-then-else'],
       'count-up_aux': ['>R', 'dup', 1, '+', '<R', 'count-up'],
       '+': [],
       '*': [],
       'repeat': [],
       'assert': ['eq', 'assertion true', 'assertion false', 'if-then-else'],
       'assert-n': ['n>R', '0--assert-n-load', 'if-then', '0--assert-n-unload', 'if-then', '<R', 'drop'],
       'assert-n-comp': ['>R', '0--assert', 'if-then', '<R', 'drop'],
       'assert-n-unload': ['dup', '>R', '0--assert', 'if-then', '<R', 'drop'],
       'if-then': [],
       'if-then-else': [],
       'timeOut': [],
       'dup': [],
       'swap': [],
       'drop': [],
       'eq': [],
       '>R': [],
       'n>R': ['dup','>Q', '0--n>R_aux', 'if-then'],
       'n>R_aux': ['>R', 'Q>',  -1, '+', 'n>R'],
       '<R': [],
       'n<R': [],
       '>Q': [],
       'n>Q': ['dup','>R', '0--n>Q_aux', 'if-then'],
       'n>Q_aux': ['>Q', '<R',  -1, '+', 'n>Q'],
       'Q>': []
       }
facts = {}
#program_list = [9, 7, '+', 2.5, '*']
#program_list = [9, 7, 'swap']
#program_list = [1,2,3, 'dup']
#program_list = [1,2,3, 'dup2']
#program_list = [9, 7, 'swap', 'dup']
#program_list = [1, 4, 'fact']
#program_list = [4, 'count-down']
#program_list = [1, 4, 'count-up']
#program_list = [1, '>R', '<R', 1, 'assert']
#program_list = [1, 2, 1, 2, 2, 'assert-n']
#program_list = [1, 2, 5, 2, 'n>R', '<R', '<R']
#program_list = [1, 2, 5, '>Q', '>Q', 'Q>', 'Q>']
program_list = [1, 2, 5, 2, 'n>Q', 'Q>', 'Q>']
#program_list = [ 4, 'yes', 'if-then', 1, 'yes', 'if-then', 0, 'no', 'yes', 'if-then-else', -1, 'yes', 'if-then']
#program_list = [0, 0, 1, 'if-then-else', 1, 'not']
#program_list = [1, 'inverse', 1.0, 'inverse', -3, 'inverse', -1.02, 'inverse']
#program_list = [1, 0, 1, '1--inverse', 'if-then-else']
#program_list = [1, 'redLED', 1, 'greenLED']
#program_list = [1, 'redLED', 1.5, 0, '1--redLED', 'timeOut']
#program_list = [ 1, 'redLED', 1, 0, '1--redLED', 'if-then', 1, 1, '1--redLED', 'if-then']
#program_list = [ 0, 'redLED', 1, 1, '1--redLED', 'if-then']
#program_list = [ 1, 0, '1--redLED', 1, '1--redLED', 'if-then-else']
# recursive example
# 4 fact
# 1 2 * 3 * 4 *
# :fact dup 1 * swap -1 + swap fact;
param_stack = []
return_stack = []
return_queue = []

def isTrue(e):
    #print('isTrue', e, (e != 0 and e != False and e != 'False'))
    if e != 0 and e != False and e != 'False':
        return True
    return False

def isValue(e, fun):
    return (isinstance(e, int) or isinstance(e, float)
            or (isinstance(e, str) and not e in fun.keys())
            )

def run(pl, vs, fun, rs, q):
    print(pl)
    while len(pl) > 0: # and not isValue(pl[-1]):
        next = pl[0];
        pl = pl[1:]
        print(vs, next)
        if isValue(next, fun):
            vs.append(next)
            continue

        if next == 'if-then':
            then_block = vs.pop()
            (then_args, then_block) = getArgs(then_block, vs)
                
            if len(vs) >= 1:
                exp = vs.pop()
            else:
                exp = False
            if isTrue(exp):
                print('if clause is True')
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
            
            if len(vs) >= 1:
                exp = vs.pop()
            else:
                exp = False
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
        
        #if next == 'repeat':
        #    repeat_block = vs.pop()
        #    (repeat_args, repeat_block) = getArgs(repeat_block, vs)
        #    if len(vs) >= 1:
        #        count = vs.pop()
        #    else:
        #        count = 0
        #    for n in range(0, count):
        #        print('repeat...')
        #        vs.extend(repeat_args)
        #        if isinstance(repeat_block, list):
        #            pl = repeat_block.extend(pl)
        #        else:
        #            pl.insert(0, repeat_block)
        #    continue
        
        
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
        
        if next == 'eq':
            v1 = vs.pop()
            v2 = vs.pop()
            vs.append(v1 == v2)
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
        
        if next == '*':
            if len(vs) < 2:
                print('Error: function '++ next ++ ' has insufficient arguments.')
                break
            lhs = vs.pop()
            rhs = vs.pop()
            vs.append(lhs * rhs)
            continue
        
        if next == '+':
            if len(vs) < 2:
                print('Error: function '++ next ++ ' has insufficient arguments.')
                break
            lhs = vs.pop()
            rhs = vs.pop()
            vs.append(lhs + rhs)
            continue
        
        if next == 'redLED':
            val = vs.pop()
            red.value = isTrue(val)
            continue
        
#        if next == 'greenLED':
#            val = vs.pop()
#            green.value = isTrue(val)
#            continue
        
        if len(next) > 2 and next[0] == '*': # and next[1]isalpha():
            vs.push(next[1:])
            continue
        
        if next in fun.keys():
            pl = fun[next] + pl
            continue
        

def getArgs(block, vs):
    args = []
    if isinstance(block, str) and block[1:3] == '--':
        # eg. 3--my-fn will consume 3 arguments and the name of the function is 'my-fn'
        arity = int(block[:1])
        block = block[3:]
        print('block', block)
        for i in range(0, arity):
            args.append(vs.pop())
    print('args', args, 'block', block )
    return (args, block)
            
print('so far so good... ready to run')
run(program_list, param_stack, fundi, return_stack, return_queue)
print(param_stack)
#while True: #loop forever
#    rs = read_rotor()
#    if rs == 1 or rs == -1:
#        stack.append(str(rs))
#        stack.append('rotary')
#        run(stack, fun)
    

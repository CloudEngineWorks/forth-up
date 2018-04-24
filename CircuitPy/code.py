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


fundi = {'rotary':{'arity': 1, 'pl':['.green', '.red', '3if']},
       'abs': {'arity': 1, 'pl':['.noop', '.inverse', '2if']},
       'inverse': {'arity': 1, 'pl':['-1', '*']},
       'noop': {'arity': 0, 'pl':[]},
       'red': {'arity': 1, 'pl':['.abs', 'redLED']},
       'green': {'arity': 1, 'pl':['.abs', 'greenLED']},
       'redLED': {'arity': 1, 'pl':[]},
       'greenLED': {'arity': 1, 'pl':[]},
       'fact': {'arity': 1, 'pl':[ '0--fact_aux', 'if-then']},
       'fact_aux': {'arity': 2, 'pl':['dup', 1, '*', 'swap', -1, '+', 'swap', 'fact']},
       '+': {'arity': 2, 'pl':[]},
       '*': {'arity': 2, 'pl':[]},
       'if-then': {'arity': 2, 'pl':[]},
       'if-then-else': {'arity': 3, 'pl':[]},
       'timeOut': {'arity': 2, 'pl':[]},
       'dup': {'arity': 1, 'pl':[]},
       'swap': {'arity': 2, 'pl':[]}
       }
facts = {}
#program_list = [9, 7, '+', 2.5, '*']
#program_list = [1, 'redLED', 1, 'greenLED']
#program_list = [ 1, 'redLED', 1.5, 0, '1--redLED', 'timeOut']
#program_list = [ 1, 'redLED', 1, 0, '1--redLED', 'if-then', 1, 1, '*redLED', 'if-then']
#program_list = [ 0, 'redLED', 1, 1, '1--redLED', 'if-then']
program_list = [ 1, 0, '1--redLED', 1, '1--redLED', 'if-then-else']
# recursive example
# 4 fact
# 1 2 * 3 * 4 *
# :fact dup 1 * swap -1 + swap fact;
value_stack = []

def isTrue(e):
    if e == '1' or e == 'True' or e == 1:
        return True
    return False

def isValue(e, fun):
    return (isinstance(e, int) or isinstance(e, float)
            or (isinstance(e, str) and not e in fun.keys())
            #or (isinstance(e, str) and len(e) > 1 and e[0] == '*') # treat a *
            )

def run(pl, vs, fun):
    print(pl)
    while len(pl) > 0: # and not isValue(pl[-1]):
        next = pl[0];
        pl = pl[1:]
        print(vs, next)
        if isValue(next, fun):
            vs.append(next)
            continue

        # if-then (a b -- ) post-fix if-then (e.g. 1 n_args n_arity_function if-then)
        if next == 'if-then':
            then_block = vs.pop()[1:]
            arity = fun[then_block]['arity']
            then_args = [5]
            for i in range(0, arity):
                then_args[i] = vs.pop()
                
            exp = vs.pop()
            if isTrue(exp):
                #print('if clause is True')
                vs.extend(then_args)
                if isinstance(then_block, list):
                    pl = then_block.extend(pl)
                else:
                    pl.insert(0, then_block)
            continue
        
        if next == 'if-then-else':
            else_block = vs.pop()[1:]
            else_arity = fun[else_block]['arity']
            else_args = [5]
            for i in range(0, else_arity):
                else_args[i] = vs.pop()
                
            then_block = vs.pop()[1:]
            then_arity = fun[then_block]['arity']
            then_args = [5]
            for i in range(0, then_arity):
                then_args[i] = vs.pop()
                
            exp = vs.pop()
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

        
        if next == 'dup':
            pl.append(pl[0])
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
            vs.extend(fun[next]['pl'])
            continue
        
            
print('so far so good...')
run(program_list, value_stack, fundi)
print(value_stack)
#while True: #loop forever
#    rs = read_rotor()
#    if rs == 1 or rs == -1:
#        stack.append(str(rs))
#        stack.append('rotary')
#        run(stack, fun)
    

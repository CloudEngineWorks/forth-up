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


fundi = {'rotary':{'arity': 1, 'pl':['0--green', '0--red', 'if-then-else']},
       'abs': {'arity': 1, 'pl':['0--noop', '0--inverse', 'if-then']},
       'inverse': {'arity': 1, 'pl':[-1, '*']},
       'not': {'arity': 1, 'pl':[0, 1, 'if-then-else']},
       'noop': {'arity': 0, 'pl':[]},
       'red': {'arity': 1, 'pl':['.abs', 'redLED']},
       'green': {'arity': 1, 'pl':['.abs', 'greenLED']},
       'redLED': {'arity': 1, 'pl':[]},
       'greenLED': {'arity': 1, 'pl':[]},
       'dup2': {'arity': 2, 'pl':[]},
       'fact': {'arity': 1, 'pl':['dup', '0--fact_aux', 'if-then']},
       'fact_aux': {'arity': 2, 'pl':['dup2', '*', 'swap', -1, '+', 'swap', 'fact']},
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
#program_list = [9, 7, 'swap']
#program_list = [1,2,3, 'dup']
#program_list = [1,2,3, 'dup2']
#program_list = [9, 7, 'swap', 'dup']
program_list = [1, 4, 'fact']
#program_list = [ 4, 'yes', 'if-then', 1, 'yes', 'if-then', 0, 'no', 'yes', 'if-then-else', -1, 'yes', 'if-then',]
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
value_stack = []

def isTrue(e):
    #print('isTrue', e, (e != 0 and e != False and e != 'False'))
    if e != 0 and e != False and e != 'False':
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
            then_block = vs.pop()
            then_args = []
            if isinstance(then_block, str) and then_block[1:3] == '--':
                # eg. 3--my-fn is an arity of 3 and the function is 'my-fn'
                then_arity = int(then_block[:1])
                then_block = then_block[3:]
                print('then-block', then_block)
                for i in range(0, then_arity):
                    then_args.append(vs.pop())
                
            exp = vs.pop()
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
            #print('else_block', else_block, else_block[1:3] == '--')
            else_args = []
            if isinstance(else_block, str) and else_block[1:3] == '--':
                else_arity = int(else_block[:1])
                else_block = else_block[3:]
                #print('else_block', else_block)
                for i in range(0, else_arity):
                    else_args.append(vs.pop())
            
            then_block = vs.pop()
            then_args = []
            if isinstance(then_block, str) and then_block[1:3] == '--':
                # eg. 3--my-fn is an arity of 3 and the function is 'my-fn'
                then_arity = int(then_block[:1])
                then_block = then_block[3:]
                #print('not a value', then_block)
                for i in range(0, then_arity):
                    then_args.append(vs.pop())
                
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
                    print('insert', else_block)
                    pl.insert(0, else_block)
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
            #vs.extend(fun[next]['pl'][:-1])
            #pl.insert(0, fun[next]['pl'][-1])
            pl.extend(fun[next]['pl'])
            continue
        
            
print('so far so good... ready to run')
run(program_list, value_stack, fundi)
print(value_stack)
#while True: #loop forever
#    rs = read_rotor()
#    if rs == 1 or rs == -1:
#        stack.append(str(rs))
#        stack.append('rotary')
#        run(stack, fun)
    

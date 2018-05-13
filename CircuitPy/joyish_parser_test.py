import joyish_parser as jp

tests = [
    ['hello world', ['hello', 'world']],
    ['"hello world"', ['hello world']],
    ['abc def eee ', ['abc', 'def', 'eee']],
    [' abc def  eee ', ['abc', 'def', 'eee']],
    ['"abc def" "123 456"', ['abc def', "123 456"]],
    ['abc "def" "123 " 456', ['abc', 'def', "123 ", 456]],
    ['5.5 2.1 + 456', [5.5, 2.1, '+', 456]],
    ['[5.5 2.1] .456 +', [[5.5, 2.1], 0.456, '+']],
    ['[[5.5 2.1] [1 2 3]] .456 +', [[[5.5, 2.1], [1, 2, 3]], 0.456, '+']],
    [' [ [5.5 2.1]  [1 2 3] ]  .456  +   ', [[[5.5, 2.1], [1, 2, 3]], 0.456, '+']],
    ['[["5.5" 2.1] [1 "2" 3]] .456 +', [[['5.5', 2.1], [1, '2', 3]], 0.456, '+']],
    [' [ ["5.5" 2.1]  [1 "2" "3 3"] ]  .456  +   ', [[['5.5', 2.1], [1, '2', '3 3']], 0.456, '+']],
    ['[4 5 +] ', [[4, 5, '+']]],
    ['[4 5 +] [4 5 +]', [[4, 5, '+'], [4, 5, '+']]],
    ['[4 5 +] [4 5 +] [4 5 +]', [[4, 5, '+'],[4, 5, '+'],[4, 5, '+']]],
    ['[4 5 +] foo [4 5 +]', [[4, 5, '+'], 'foo', [4, 5, '+']]],
    ['{a:5.5 b:2.1} .456 +', [{"a":5.5, "b":2.1}, 0.456, '+']],
    [' {a:5.5 b:2.1} .456 +', [{"a":5.5, "b":2.1}, 0.456, '+']],
    ['{ a:5.5 b:2.1} .456 +', [{"a":5.5, "b":2.1}, 0.456, '+']],
    [' { a:5.5  b:2.1 } .456 +', [{"a":5.5, "b":2.1}, 0.456, '+']],
]

def cmpLists(a, b):
    same = True
    if len(a) == len(b):
        for i in range(len(a)):
            if a[i] != b[i]:
                same = False
    else:
        same = False
    return same
    
print('Starting parser tests:')
anyFailed = False
for test in tests:
    ps = test[0]
    expected_stack = test[1]
    
    #print('starting parse test for: ', ps)
    result_stack = jp.parse(ps)
    
    if not cmpLists(result_stack, expected_stack):
        anyFailed = True
        print(result_stack, ' expected:', expected_stack)
        print('---- Failed parse test for: ', ps)
if not anyFailed:
    print('All tests passed')

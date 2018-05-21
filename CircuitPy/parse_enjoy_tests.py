
from joyish_parser import parse
from joyish_tests import tests

parsed_tests = []
for test in tests:
    ps = test[0]
    parsed_tests.append([parse(ps), test[1]])
    
print('tests =', parsed_tests)
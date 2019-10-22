""" return vs. yeild test"""

def return_test(anylist):
    for i in anylist:
        return i


def yield_test(anylist):
    for i in anylist:
        yield i

int_list = [1,2,3,4,5,6,7,8,9]

"""just printing the result of the function"""

print "return_test on int_list =", return_test(int_list)

print "yield_test on int_list =", yield_test(int_list)

"""using itiration"""

print "return_test using iteration =",

try:
    for i in return_test(int_list):
        print i
except TypeError:
    print "'Error Msg: int' object is not iterable"

print "yield_test using iteration ="

for i in yield_test(int_list):
    print i

"""The function using return can only return a single integer\
because the function finishes as soon as it hits return.\
The yield function creates a generator object that you have to manipulate\
in a special way to access properly (iteration).\
Using iteration doesn't work for the return function,\
because it only returns a single integer, which is not iterable.
The yield function however, is able to generate the next integer\
in the sequence each time through until it hits the end of the list."""



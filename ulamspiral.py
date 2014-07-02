################################################################################
#
# A simple program for visualising Ulam's Spiral.
# Makes use of PIL (via pillow) for generating computer graphics.
#
# AUTHOR: Yoshua Wakeham
#
#    - SimpleImage (by Bernie Pope)
#         http://ww2.cs.mu.oz.au/~bjpop/comp10001-2013s2/
#         projects/proj2/SimpleImage.py
#
################################################################################

import sys
from math import sqrt
from types import *
from SimpleImage import write_image

BLACK = (  0,  0,  0)
WHITE = (255,255,255)
RED   = (255,  0,  0)
GREEN = (  0,255,  0)
BLUE  = (  0,  0,255)

#dir  = (row offset, col offset)
NORTH = (-1,0)
WEST  = (0,-1)
SOUTH = (1, 0)
EAST  = (0, 1)

dirs  = [NORTH,WEST,SOUTH,EAST]

### FUNCTIONS ###

def prime_sieve(bound):
    '''
    An implementation of the Sieve of Eratosthenes for
    generating a list of all the prime numbers up to
    some bounding value.
    '''
    assert type(bound) is IntType,\
            "upper bound is not an integer: {}".format(bound)
    list = [1] * bound
    # eliminate even numbers above 2
    for i in range(3,bound,2):
        list[i] = 0
    # main sieve
    for i in range(3,int(sqrt(bound))):
        if list[i-1]:
            for j in range(i**2,bound+1,2*i):
                list[j-1] = 0
    return list

def is_prime(n, prime_list):
    '''
    Tests an integer for primality, assuming a list
    of primes has already been generated in which
    primes[n] evaluates to True if n is prime.
    '''
    assert type(n) is IntType,\
            "cannot test primality of non-integer: {}".format(n)
    assert type(prime_list) is ListType,\
            "not a list: {}".format(prime_list)
    if prime_list[n-1]:
        return True
    else:
        return False

def spiral(image,size,lower,upper,primes):
    history = []
    for i in range(size[0]):
        history.append([0]*size[1])
    location = (size[0]/2,size[1]/2)
    orientation = NORTH
    paintcell(image,location,WHITE)
    history[location[0]][location[1]] = 1
    location = advance(location,orientation)
    for n in range(lower+1,upper+1):
        if is_prime(n,primes):
            paintcell(image,location,BLUE)
        history[location[0]][location[1]] = 1
        my_left = getleft(location,orientation)
        if history[my_left[0]][my_left[1]] == 0:
            orientation = turnleft(orientation)
        location = advance(location,orientation)

def paintcell(image,location,colour):
    image[location[0]][location[1]] = colour

def advance(location,orientation):
    rowoffset = orientation[0]
    coloffset = orientation[1]
    return (location[0]+rowoffset,location[1]+coloffset)

def turnleft(orientation):
    index = (dirs.index(orientation)+1)%4
    return dirs[index]

def getleft(location,orientation):
    if orientation in [NORTH,SOUTH]:
        rowoffset = orientation[1]
        coloffset = orientation[0]
    else:
        rowoffset = -(orientation[1])
        coloffset = -(orientation[0])
    return (location[0]+rowoffset,location[1]+coloffset)
    
### MAIN ###
if __name__ == '__main__':
    argc = len(sys.argv)
    if not (2 <= argc <= 3):
        print("ulamspiral: usage: python ulamspiral.py [lower] upper")
        print("where 'lower' and 'upper' are integers.")
        exit()

    if argc == 3:
        lower = int(sys.argv[1])
        upper = int(sys.argv[2])
    else:
        lower = 1
        upper = int(sys.argv[1])

    primes = prime_sieve(upper)
    num_cells = upper - lower + 1
    size = (int(sqrt(num_cells))+1,int(sqrt(num_cells))+1)

    image = []
    for i in range(size[0]):
        image.append([BLACK]*size[1])

    spiral(image,size,lower,upper,primes)

    write_image(image,"ulamspiral_{0}-{1}.png".format(lower,upper))


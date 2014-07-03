###############################################################################
#
# ::: ULAMSPIRAL :::
#
# AUTHOR: Yoshua Wakeham
#
#    Yoshua Wakeham
#        email: yoshwakeham@gmail.com
#        www  : github.com/yoshw
#        tweet: @yoshw
#
#    SimpleImage module by Bernie Pope, 2012
#        http://ww2.cs.mu.oz.au/~bjpop/comp10001-2013s2/
#        projects/proj2/SimpleImage.py
#
# DATE CREATED
#
#    3 July 2014
#
# NOTES
#
#    Ulamspiral is a simple program for generating Ulam spirals.
#    (See https://en.wikipedia.org/wiki/Ulam_spiral)
#
#    It makes use of PIL (via Bernie Pope's SimpleImage) to output
#    a PNG file wherein each pixel represents an integer determined
#    by the 'spiralling' Ulam pattern. If the integer is prime, the
#    pixel is coloured; otherwise it is black.
#
# COPYING
#
#    This program is free software: you can redistribute it
#    and/or modify it under the terms of the GNU General Public
#    License as published by the Free Software Foundation, either
#    version 3 of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import sys
import code.pymodules.primes as prm
from SimpleImage import write_image, get_width, get_height


### CONSTANTS #################################################################

#         Red  Grn  Blu
BLACK = (   0,   0,   0)
WHITE = ( 255, 255, 255)
RED =   ( 255,   0,   0)
GREEN = (   0, 255,   0)
BLUE =  (   0,   0, 255)

#        row offset  col offset
NORTH = (        -1,          0)
WEST =  (         0,         -1)
SOUTH = (         1,          0)
EAST =  (         0,          1)


### FUNCTIONS #################################################################

def prime_sieve(bound):
    '''
    An implementation of the Sieve of Eratosthenes:
    generates a list of all the prime numbers up to
    some bounding value.
    '''
    try:
        list = [1] * bound
    except:
        print("Error: upper bound is not an integer: {}".format(bound))

    # sieve even numbers greater than 2
    for i in range(3, bound, 2):
        list[i] = 0
    # sieve remaining composites
    for i in range(3, int(sqrt(bound))):
        if list[i-1]:
            for j in range(i**2, bound+1, 2*i):
                list[j-1] = 0
    return list


def is_prime(n, prime_list):
    '''
    Tests an integer for primality, assuming a list
    of primes has already been generated in which
    primes[n-1] evaluates to True if n is prime.
    '''
    try:
        test = prime_list[n-1]
    except TypeError:
        print("Error: invalid input to is_prime() function")

    return bool(test)


def spiral(image, lower, upper, primes):
    height = get_height(image)
    width = get_width(image)

    # make a new two-dimensional list, equal in size
    # to the image, to record which pixels the spiral
    # has already visited
    trail = [[0]*width for _i in range(height)]
    # initialise spiral
    row, col = (height/2, width/2)
    orientn = NORTH
    # paint initial cell (and record that the spiral
    # was here, then move to second cell
    paintcell(image, row, col, WHITE)
    trail[row][col] = 1
    row, col = advance(row, col, orientn)

    for n in range(lower+1, upper+1):
        if prm.is_sieved_prime(n, primes):
            paintcell(image, row, col, BLUE)
        trail[row][col] = 1
        lrow, lcol = getleft(row, col, orientn)
        if trail[lrow][lcol] == 0:
            orientn = turnleft(orientn)
        row, col = advance(row, col, orientn)


def paintcell(image, row, col, colour):
    image[row][col] = colour


def advance(row, col, orientn):
    rowoffset = orientn[0]
    coloffset = orientn[1]
    return row + rowoffset, col + coloffset


def turnleft(orientn):
    dirs = [NORTH, WEST, SOUTH, EAST]
    index = (dirs.index(orientn) + 1) % 4
    return dirs[index]


def getleft(row, col, orientn):
    if orientn in [NORTH, SOUTH]:
        rowoffset = orientn[1]
        coloffset = orientn[0]
    else:
        rowoffset = -(orientn[1])
        coloffset = -(orientn[0])
    return row + rowoffset, col + coloffset


### MAIN #################################################################

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

    primes = prm.prime_sieve(upper)
    num_cells = upper - lower + 1
    width = height = int(sqrt(num_cells)) + 1

    image = [[BLACK]*width for _i in range(height)]

    spiral(image, lower, upper, primes)

    write_image(image, "ulamspiral_{0}-{1}.png".format(lower, upper))

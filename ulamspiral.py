###############################################################################
#
# ::: ULAMSPIRAL :::
#
# AUTHORS
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
#    (See https://en.wikipedia.org/wiki/Ulam_spiral for details.)
#
#    It makes use of PIL (via Bernie Pope's SimpleImage) to output
#    a PNG file wherein each pixel represents an integer determined
#    by the 'spiralling' Ulam pattern. If the integer is prime, the
#    pixel is coloured; otherwise it is black.
#
#    This code is designed to be run with Python 2.7x. It was
#    written and tested on a MacBook Pro running OSX 10.9 Mavericks.
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
# CHANGE LOG
#
#    9 Jul 14: added docstrings, comments
#
###############################################################################

import sys
import primes.primes as prm
from math import sqrt
from SimpleImage.SimpleImage import write_image


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

def spiral(image, lower, upper, primes):
    """
    spiral(image, int, int, list) -> None

    Takes an image (a rectangular list of lists), lower
    and upper bounds (integers), and a list of the prime
    numbers (assumed to be) in the range 1 - upper.

    Modifies the input image by traversing it according
    to the pattern of Ulam's spiral, starting in the centre
    of the image and moving out in CCW fashion. Each pixel
    is assigned an integer, beginning with the lower bound.
    If the integer is prime, the pixel is painted; otherwise
    it is left unchanged.
    """
    # get image dimensions
    height = len(image)
    if height == 0:
        width = 0
    else:
        width = len(image[0])
    # make a new two-dimensional list, equal in size
    # to the image, to record which pixels the spiral
    # has already visited
    trail = [[0]*width for _i in range(height)]
    # initialise spiral
    row, col = (height/2, width/2)
    orientn = NORTH
    # paint initial cell (and record that the spiral
    # was here), then move to second cell
    paintcell(image, row, col, WHITE)
    trail[row][col] = 1
    row, col = advance(row, col, orientn)
    # proceed along the spiral until upper
    # bound is reached
    for n in range(lower+1, upper+1):
        if prm.is_sieved_prime(n, primes):
            paintcell(image, row, col, BLUE)
        trail[row][col] = 1
        lrow, lcol = getleft(row, col, orientn)
        if trail[lrow][lcol] == 0:
            orientn = turnleft(orientn)
        row, col = advance(row, col, orientn)


def paintcell(image, row, col, colour):
    """
    paintcell(image, int, int, colour) -> None

    Changes the colour of the pixel at the specified
    row and column of the input image. The image must
    be a rectangular list of lists, with parameter 'colour'
    having the same format as the pixels of the image.
    """
    image[row][col] = colour


def advance(row, col, orientn):
    """
    advance(int, int, orientation) -> new coordinates (int, int)

    Moves the spiral one cell 'forward'.

    The orientation is assumed to be a 2-tuple
    storing offset information for traversing an image
    stored as a rectangular list of lists. This accounts
    for the fact that 'advancing' mutates co-ordinates in
    different ways depending on orientation.

    Returns a 2-tuple with the updated row/col co-ordinates.
    """
    rowoffset = orientn[0]
    coloffset = orientn[1]
    return row + rowoffset, col + coloffset


def turnleft(orientn):
    """
    turnleft(orientation) -> new orientation

    Returns the orientation which results from a 'left turn'.
    Assumes that orientations have been predefined.
    """
    dirs = [NORTH, WEST, SOUTH, EAST]
    index = (dirs.index(orientn) + 1) % 4
    return dirs[index]


def getleft(row, col, orientn):
    """
    getleft(int, int, orientation) -> cell co-ordinates (int, int)

    Get row/col co-ordinates of cell to the left of current
    location. The orientation is assumed to be a 2-tuple
    storing offset information for traversing an image
    stored as a rectangular list of lists. This accounts
    for the fact that 'left' is relative to orientation.
    Returns a 2-tuple with the co-ords of the required cell.
    """
    if orientn in [NORTH, SOUTH]:
        rowoffset = orientn[1]
        coloffset = orientn[0]
    else:
        rowoffset = -(orientn[1])
        coloffset = -(orientn[0])
    return row + rowoffset, col + coloffset


### MAIN ROUTINE #########################################################

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
        # only one bound supplied
        lower = 1
        upper = int(sys.argv[1])

    if lower >= upper:
        print("error: lower bound must be strictly lower than upper bound")
        exit()

    # generate a list of primes from 1 to upper
    primes = prm.prime_sieve(upper)
    # total number of pixels required
    num_cells = upper - lower + 1
    # define image size accordingly
    width = height = int(sqrt(num_cells)) + 1

    image = [[BLACK]*width for _i in range(height)]

    spiral(image, lower, upper, primes)

    write_image(image, "ulamspiral_{0}-{1}.png".format(lower, upper))

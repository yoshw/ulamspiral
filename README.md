# Ulamspiral

## What is it?

A simple script for generating Ulam spirals,
which are visualisations of patterns in the prime
numbers. A lower and upper bound for the spiral
may be specified; these bounds determine the
range of integers whose primality will be
visualised.

The spirals are generated as PNG images,
using PIL (via pillow).

## Usage

Ulamspiral is a command-line tool. Run it with

    $ python ulamspiral.py [LOWER] UPPER

where LOWER and UPPER are both integers, with LOWER
optional. If both bounds are supplied, UPPER must be
strictly greater than LOWER.

Alternatively, `import ulamspiral` to access its functions.

## License

ulamspiral is free software: you can redistribute it
and/or modify it under the terms of the GNU General Public
License. See module header and GPL.txt for more detail.

## Contact

Yoshua Wakeham
* email: yoshwakeham@gmail.com

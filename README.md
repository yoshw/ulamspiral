# Ulamspiral

### What is it?

A simple script for generating Ulam spirals,
which are visualisations of patterns in the prime
numbers. A lower and upper bound for the spiral
may be specified; these bounds determine the
range of integers whose primality will be
visualised. Each pixel in the generated image
represents an integer. If the integer is prime,
the pixel will be coloured (blue, by default).
Otherwise, the pixel will be black.

The spirals are generated as PNG images,
using PIL (via Bernie Pope's SimpleImage.py
-- see module header for URL).

### Usage

Ulamspiral is a command-line tool. Run it with

    $ python ulamspiral.py [LOWER] UPPER

where LOWER and UPPER are both integers, with LOWER
optional (defaulting to 1 if unspecified). If both bounds
are supplied, UPPER must be strictly greater than LOWER.

Alternatively, `import ulamspiral` within a Python
module to access its functions.

### License

Ulamspiral is free software: you can redistribute it
and/or modify it under the terms of the GNU General Public
License. See module header and GPL.txt for more detail.

### Contact

Yoshua Wakeham
* email: yoshwakeham@gmail.com

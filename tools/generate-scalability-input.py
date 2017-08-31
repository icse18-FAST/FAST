'''
This file is part of an ICSE'18 submission that is currently under review. 
For more information visit: https://github.com/icse18-FAST/FAST.
    
This is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.

This software is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this source.  If not, see <http://www.gnu.org/licenses/>.
'''

import random
import sys


usage = """USAGE: python py/generate-scalability-input.py <tssize> <tcsize>
OPTIONS:
  <tssize>: number of test cases in the test suite.
    options: a positive integer, e.g. 1000.
  <tcsize>: size of the test cases.
    options: small, medium, large"""


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Wrong input.")
        print(usage)
        exit()
    ts_size, tc_size = sys.argv[1:]
    ts_size = int(ts_size)

    tcsizes = {'small', 'medium', 'large'}
    tc_map = {
        'small': 1000,
        'medium': 10000,
        'large': 100000
    }

    if ts_size <= 0:
        print("<tcsize> input incorrect.")
        print(usage)
        exit()
    elif tc_size not in tcsizes:
        print("<tssize> input incorrect.")
        print(usage)
        exit()


    tc_size = tc_map[tc_size]
    minp, maxp = 0.075, 0.125

    filename = "scalability/input/{}x{}.txt".format(ts_size, tc_size)
    with open(filename, "w") as fout:
        for tc in xrange(1, ts_size + 1):
            line = ""
            mincov, maxcov = minp * tc_size, maxp * tc_size
            cov = set()
            for _ in xrange(random.randrange(mincov, maxcov)):
                cov.add(random.randint(1, tc_size + 1))
            for st in sorted(cov):
                line += str(st) + " "
            fout.write(line.strip() + "\n")

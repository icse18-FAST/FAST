import random
import sys


usage = """USAGE: python py/generate-scalability-input.py <tssize> <tcsize> <algorithm>
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

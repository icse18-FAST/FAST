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

import math
import os
import sys

import competitors
import fast


usage = """USAGE: python py/scalability.py <tssize> <tcsize> <algorithm>
OPTIONS:
  <tssize>: number of test cases in the test suite.
    options: a positive integer, e.g. 1000.
  <tcsize>: size of the test cases.
    options: small, medium, large
  <algorithm>: algorithm used for prioritization.
    options: FAST-pw, FAST-one, FAST-log, FAST-sqrt, FAST-all, STR, I-TSD, ART-D, ART-F, GT, GA, GA-S"""


def scalability(name, ts, tc, n, r, b, selsize):
    filename = "{}x{}".format(ts, tc)
    fin = "scalability/input/{}.txt".format(filename)
    outpath = "scalability/output/"


    if name == "FAST-" + selsize.__name__[:-1]:
        if ("{}-{}.tsv".format(name, filename)) not in set(os.listdir(outpath)):
            stime, ptime, prioritization = fast.fast_(
                fin, selsize, r=r, b=b, memory=False)
            print("  Progress: 100%  ")
            print "  Running time:", stime + ptime
            rep = (name, stime, ptime)
            writeOutput(outpath, filename, rep)
        else:
            print name, "already run."

    elif name == "FAST-pw":
        if ("{}-{}.tsv".format(name, filename)) not in set(os.listdir(outpath)):
            stime, ptime, prioritization = fast.fast_pw(
                fin, selsize, r=r, b=b, memory=False)
            print("  Progress: 100%  ")
            print "  Running time:", stime + ptime
            rep = (name, stime, ptime)
            writeOutput(outpath, filename, rep)
        else:
            print name, "already run."

    elif name == "STR":
        if ("{}-{}.tsv".format(name, filename)) not in set(os.listdir(outpath)):
            print name
            stime, ptime, prioritization = competitors.str_(fin)
            print("  Progress: 100%  ")
            print "  Running time:", stime + ptime
            rep = (name, stime, ptime)
            writeOutput(outpath, filename, rep)
            print("")
        else:
            print name, "already run."

    elif name == "I-TSD":
        if ("{}-{}.tsv".format(name, filename)) not in set(os.listdir(outpath)):
            print name
            stime, ptime, prioritization = competitors.i_tsd(fin)
            print("  Progress: 100%  ")
            print "  Running time:", stime + ptime
            rep = (name, stime, ptime)
            writeOutput(outpath, filename, rep)
            print("")
        else:
            print name, "already run."

    elif name == "GT":
        if ("{}-{}.tsv".format(name, filename)) not in set(os.listdir(outpath)):
            print name
            stime, ptime, prioritization = competitors.gt(fin)
            print("  Progress: 100%  ")
            print "  Running time:", stime + ptime
            rep = (name, stime, ptime)
            writeOutput(outpath, filename, rep)
            print("")
        else:
            print name, "already run."

    elif name == "GA":
        if ("{}-{}.tsv".format(name, filename)) not in set(os.listdir(outpath)):
            print name
            stime, ptime, prioritization = competitors.ga(fin)
            print("  Progress: 100%  ")
            print "  Running time:", stime + ptime
            rep = (name, stime, ptime)
            writeOutput(outpath, filename, rep)
            print("")
        else:
            print name, "already run."

    elif name == "GA-S":
        if ("{}-{}.tsv".format(name, filename)) not in set(os.listdir(outpath)):
            print name
            stime, ptime, prioritization = competitors.ga_s(fin)
            print("  Progress: 100%  ")
            print "  Running time:", stime + ptime
            rep = (name, stime, ptime)
            writeOutput(outpath, filename, rep)
            print("")
        else:
            print name, "already run."

    elif name == "ART-D":
        if ("{}-{}.tsv".format(name, filename)) not in set(os.listdir(outpath)):
            print name
            stime, ptime, prioritization = competitors.art_d(fin)
            print("  Progress: 100%  ")
            print "  Running time:", stime + ptime
            rep = (name, stime, ptime)
            writeOutput(outpath, filename, rep)
            print("")
        else:
            print name, "already run."

    elif name == "ART-F":
        if ("{}-{}.tsv".format(name, filename)) not in set(os.listdir(outpath)):
            print name
            stime, ptime, prioritization = competitors.art_f(fin)
            print("  Progress: 100%  ")
            print "  Running time:", stime + ptime
            rep = (name, stime, ptime)
            writeOutput(outpath, filename, rep)
            print("")
        else:
            print name, "already run."

    else:
        print "Wrong input name."


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def writeOutput(outpath, filename, res):
    name, st, pt = res
    with open("{}{}-{}.tsv".format(outpath, name, filename), "w") as fout:
        fout.write("SignatureTime\tPrioritizationTime\n")
        fout.write("{}\t{}\n".format(st, pt))


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Wrong input.")
        print(usage)
        exit()
    ts, tcsize, algname = sys.argv[1:]
    ts = int(ts)

    tcsizes = {'small', 'medium', 'large'}
    tc_map = {
        'small': 1000,
        'medium': 10000,
        'large': 100000
    }
    algnames = {"FAST-pw", "FAST-one", "FAST-log", "FAST-sqrt", "FAST-all",
                "STR", "I-TSD",
                "ART-D", "ART-F", "GT", "GA", "GA-S"}

    if algname not in algnames:
        print("<algorithm> input incorrect.")
        print(usage)
        exit()
    elif ts <= 0:
        print("<tcsize> input incorrect.")
        print(usage)
        exit()
    elif tcsize not in tcsizes:
        print("<tssize> input incorrect.")
        print(usage)
        exit()

    tc = tc_map[tcsize]


    directory = "scalability/input/"
    filename = "{}x{}.txt".format(ts, tc)
    if not os.path.exists(directory):
        print "No input folder."
        exit()
    if (filename) not in set(os.listdir(directory)):
        print "No input file:", directory + filename
        print "The file can be generated using\n  python tools/generate-scalability-input.py <tssize> <tcsize>"
        exit()

    # FAST parameters
    n, r, b = 10, 1, 10

    # FAST-f sample size
    if algname == "FAST-all":
        def all_(x): return x
        selsize = all_
    elif algname == "FAST-sqrt":
        def sqrt_(x): return int(math.sqrt(x)) + 1
        selsize = sqrt_
    elif algname == "FAST-log":
        def log_(x): return int(math.log(x, 2)) + 1
        selsize = log_
    elif algname == "FAST-one":
        def one_(x): return 1
        selsize = one_
    else:
        def pw(x): pass
        selsize = pw

    scalability(algname, ts, tc, n, r, b, selsize)

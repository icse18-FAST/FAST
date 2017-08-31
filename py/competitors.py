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

# WHITE BOX PRIORITIZATIONS
# GreedyTotal, GreedyAdditional, AdditionalSpanning, Jiang, Zhou

# BLACK BOX PRIORITIZATIONS
# Ledru, I-TSD

from collections import defaultdict
from collections import OrderedDict
from pickle import dump, load
from struct import pack, unpack
import bz2
import itertools
import math
import os
import random
import time
import scipy.special  # ledru statistics
import subprocess
import sys

import lsh


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def loadTestSuite(input_file, bbox=False, k=5):
    """INPUT
    (str)input_file: path of input file
    (bool)bbox: apply k-shingles to input
    (int)k: k-shingle size

    OUTPUT
    (dict)TS: key=tc_ID, val=set(covered lines/shingles)"""
    TS = {}
    with open(input_file) as fin:
        tcID = 1
        for tc in fin:
            if bbox:
                TS[tcID] = tc[:-1]
            else:
                TS[tcID] = set(tc[:-1].split())
            tcID += 1
    shuffled = TS.items()
    random.shuffle(shuffled)
    TS = OrderedDict(shuffled)
    if bbox:
        TS = lsh.kShingles(TS, k)
    return TS


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# GREEDY SET COVER (TOTAL)
def gt(input_file):
    def loadTestSuite(input_file):
        TS = {}
        with open(input_file) as fin:
            tcID = 1
            for tc in fin:
                TS[tcID] = len(set(tc[:-1].split()))
                tcID += 1
        shuffled = TS.items()
        random.shuffle(shuffled)
        TS = OrderedDict(shuffled)
        return TS

    ptime_start = time.clock()

    TCS = loadTestSuite(input_file)
    TS = OrderedDict(sorted(TCS.items(), key=lambda t: -t[1]))

    ptime = time.clock() - ptime_start

    return 0.0, ptime, TS.keys()


# GREEDY SET COVER (ADDITIONAL)
def ga(input_file):
    def select(TS, U, Cg):
        s, uncs_s = 0, -1
        for ui in U:
            uncs = len(TS[ui] - Cg)
            if uncs > uncs_s:
                s, uncs_s = ui, uncs
        return s

    ptime_start = time.clock()

    TCS = loadTestSuite(input_file)
    TS = OrderedDict(sorted(TCS.items(), key=lambda t: -len(t[1])))
    U = TS.copy()
    Cg = set()

    TS[0] = set()
    P = [0]

    maxC = len(reduce(lambda x, y: x | y, TS.values()))

    while len(U) > 0:
        if len(Cg) == maxC:
            Cg = set()
        s = select(TS, U, Cg)
        P.append(s)
        Cg = Cg | U[s]
        del U[s]

    ptime = time.clock() - ptime_start

    return 0.0, ptime, P[1:]


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# JIANG (ART)
# dynamic candidate set
def artd(input_file):
    def generate(U):
        C, T = set(), set()
        while True:
            ui = random.choice(U.keys())
            S = U[ui]
            if T | S == T:
                break
            T = T | S
            C.add(ui)
        return C

    def select(TS, P, C):
        D = {}
        for cj in C:
            D[cj] = {}
            for pi in P:
                D[cj][pi] = lsh.jDistance(TS[pi], TS[cj])
        # maximum among the minimum distances
        j, jmax = 0, -1
        for cj in D.keys():
            min_di = min(D[cj].values())
            if min_di > jmax:
                j, jmax = cj, min_di
        return j

    # # # # # # # # # # # # # # # # # # # # # #

    ptime_start = time.clock()

    TS = loadTestSuite(input_file)
    U = TS.copy()

    TS[0] = set()
    P = [0]

    C = generate(U)

    iteration, total = 0, float(len(U))
    while len(U) > 0:
        iteration += 1
        if iteration % 100 == 0:
            sys.stdout.write("  Progress: {}%\r".format(
                round(100*iteration/total, 2)))
            sys.stdout.flush()

        if len(C) == 0:
            C = generate(U)
        s = select(TS, P, C)
        P.append(s)
        del U[s]
        C = C - set([s])

    ptime = time.clock() - ptime_start

    return 0.0, ptime, P[1:]


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# ZHOU
# fixed size candidate set + manhattan distance
def artf(input_file):
    def generate(U):
        C = set()
        if len(U) < 10:
            C = set(U.keys())
        else:
            while len(C) < 10:
                ui = random.choice(U.keys())
                C.add(ui)
        return C

    def manhattanDistance(TCS, i, j):
        u, v = TCS[i], TCS[j]
        return sum([abs(float(ui) - float(vi)) for ui, vi in zip(u, v)])

    def select(TS, P, C):
        D = {}
        for cj in C:
            D[cj] = {}
            for pi in P:
                D[cj][pi] = manhattanDistance(TS, pi, cj)
        # maximum among the minimum distances
        j, jmax = 0, -1
        for cj in D.keys():
            min_di = min(D[cj].values())
            if min_di > jmax:
                j, jmax = cj, min_di

        return j

    # # # # # # # # # # # # # # # # # # # # # #

    ptime_start = time.clock()

    TS = loadTestSuite(input_file)
    U = TS.copy()

    TS[0] = set()
    P = [0]

    C = generate(U)

    iteration, total = 0, float(len(U))
    while len(U) > 0:
        iteration += 1
        if iteration % 100 == 0:
            sys.stdout.write("  Progress: {}%\r".format(
                round(100*iteration/total, 2)))
            sys.stdout.flush()

        if len(C) == 0:
            C = generate(U)
        s = select(TS, P, C)
        P.append(s)
        del U[s]
        C = C - set([s])

    ptime = time.clock() - ptime_start

    return 0.0, ptime, P[1:]


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# WHITEBOX ONLY
# ADDITIONAL SPANNING (LINE, BRANCH, FUNCTION)
def ga_s(input_file):
    def storeSpanningFile(input_file, spanfile):
        TCS = loadTestSuite(input_file)
        matrixFile = "{}.mat".format(spanfile)
        with open(matrixFile, "w") as fout:
            for tcID, tc in TCS.items():
                for cov in tc:
                    fout.write("{} {}\n".format(cov, tcID))

        # subsume.pl perl script process files and creates spanningEntityFile
        with open(spanfile + ".tmp", "w") as fout:
            subprocess.call(["perl", "py/subsume.pl", matrixFile], stdout=fout)
        os.remove(matrixFile)

        # compute spanning file
        with open(spanfile + ".tmp") as fin:
            spans = {line.strip() for line in fin}
            for tcID, tc in TCS.items():
                TCS[tcID] = tc & spans
        os.remove(spanfile + ".tmp")

        # store spanning file
        with open(spanfile, "w") as fout:
            for tcID in xrange(1, len(TCS)):
                fout.write(" ".join(TCS[tcID]) + "\n")

    def select(TS, U, Cg):
        s, uncs_s = 0, -1
        for ui in U:
            uncs = len(TS[ui] - Cg)
            if uncs > uncs_s:
                s, uncs_s = ui, uncs
        return s

    # # # # # # # # # # # # # # # # # # # # # # # # # # #

    spanfile = input_file.replace(".txt", ".span")
    spantimefile = "{}_spantime.txt".format(input_file.split(".")[0])
    if not os.path.exists(spanfile):
        # time.clock() does not consider subprocess call time
        span_t = time.time()
        storeSpanningFile(input_file, spanfile)
        stime = time.time() - span_t
        with open(spantimefile, "w") as fout:
            fout.write(repr(stime))
    else:
        with open(spantimefile, "r") as fin:
            stime = eval(fin.read().replace("\n", ""))

    ptime_start = time.clock()
    TCS = loadTestSuite(spanfile)

    TS = OrderedDict(sorted(TCS.items(), key=lambda t: -len(t[1])))
    U = TS.copy()
    Cg = set()

    TS[0] = set()
    P = [0]

    maxC = len(reduce(lambda x, y: x | y, TS.values()))

    iteration, total = 0, float(len(TCS))
    while len(U) > 0:
        iteration += 1
        if iteration % 100 == 0:
            sys.stdout.write("  Progress: {}%\r".format(
                round(100*iteration/total, 2)))
            sys.stdout.flush()

        if len(Cg) == maxC:
            Cg = set()
        s = select(TS, U, Cg)
        P.append(s)
        Cg = Cg | U[s]
        del U[s]

    ptime = time.clock() - ptime_start

    return stime, ptime, P[1:]


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# BLACK BOX
def str_(input_file):
    def loadTestSuite(input_file):
        TS = {}
        maxlen = 0
        with open(input_file) as fin:
            tcID = 1
            for tc in fin:
                if len(tc) > maxlen:
                    maxlen = len(tc)
                TS[tcID] = tc[:-1]
                tcID += 1
        for tcID, tc in TS.items():
            asciivec = []
            for c in tc:
                asciivec.append(float(ord(c)))
            asciivec += [0.0] * (maxlen - len(tc))
            TS[tcID] = asciivec
        shuffled = TS.items()
        random.shuffle(shuffled)
        return OrderedDict(shuffled)

    def manhattanDistance(TCS, i, j):
        u, v = TCS[i], TCS[j]
        return sum([abs(float(ui) - float(vi)) for ui, vi in zip(u, v)])

    def storePairwiseDistance(TCS, sigfile):
        D = defaultdict(float)
        combs = scipy.special.binom(len(TCS.keys()), 2)
        iteration, total = 0, float(combs)
        for pair in itertools.combinations(TCS.keys(), 2):
            # print iteration, total
            iteration += 1
            if iteration % 100 == 0:
                sys.stdout.write("  Progress: {}%\r".format(
                    round(100*iteration/total, 2)))
                sys.stdout.flush()

            i, j = pair
            if i < j:
                D[(i, j)] = manhattanDistance(TCS, i, j)
        dump(D, open(sigfile, "wb"))

    def loadPairwiseDistance(sigfile):
        return load(open(sigfile, "rb"))

    def removeDuplicates(TCS):
        unique = set()
        P = []
        for tcID, tc in TCS.items():
            tc = tuple(tc)
            if tc in unique:
                P.append(tcID)
            else:
                unique.add(tc)
        for tc in P:
            del TCS[tc]
        return P

    def select(TCS, D, T):
        s, dist_s = 0, -1
        for ui in TCS:
            dist = float("Inf")
            for vi in T:
                if ui < vi and D[(ui, vi)] < dist:
                    dist = D[(ui, vi)]
            if dist > dist_s:
                s, dist_s = ui, dist
        return s

    # # # # # # # # # # # # # # # # # # # # # # #

    TCS = loadTestSuite(input_file)
    P1 = []

    sigfile = input_file.replace(".txt", "___.pickle").replace("___", "_distmatrix")
    if not os.path.exists(sigfile):
        ledru_t = time.clock()
        storePairwiseDistance(TCS, sigfile)
        ledru_time = time.clock() - ledru_t
        with open("{}_sigtime.txt".format(input_file.split(".")[0]), "w") as fout:
            fout.write(repr(ledru_time))
    else:
        with open("{}_sigtime.txt".format(input_file.split(".")[0]), "r") as fin:
            ledru_time = eval(fin.read().replace("\n", ""))

    ptime_start = time.clock()
    load_time_start = time.clock()
    D = loadPairwiseDistance(sigfile)

    P2 = removeDuplicates(TCS)

    s = select(TCS, D, TCS.keys())
    P1.append(s)
    del TCS[s]

    iteration, total = 0, float(len(TCS))
    while len(TCS) > 0:
        iteration += 1
        if iteration % 100 == 0:
            sys.stdout.write("  Progress: {}%\r".format(
                round(100*iteration/total, 2)))
            sys.stdout.flush()

        s = select(TCS, D, P1)
        P1.append(s)
        del TCS[s]

    ptime = time.clock() - ptime_start

    return ledru_time, ptime, P1 + P2


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# I-TSD
def i_tsd(input_file):
    def loadTestSuite(input_file):
        TS = {}
        with open(input_file) as fin:
            tcID = 1
            for tc in fin:
                TS[tcID] = tc[:-1]
                tcID += 1
        shuffled = TS.items()
        random.shuffle(shuffled)
        TS = OrderedDict(shuffled)
        return TS

    def compressExcept(TCS, toExclude):
        s = " ".join([TCS[tcID] for tcID in TCS.keys() if tcID != toExclude])
        cs = bz2.compress(s)
        return sys.getsizeof(cs)

    def select(TCS):
        maxIndex, maxCompress = 0, 0
        for tcID in TCS.keys():
            c = compressExcept(TCS, tcID)
            if c > maxCompress:
                maxIndex, maxCompress = tcID, c
        return maxIndex

    # # # # # # # # # # # # # # # # # # # # # # # # # # #

    stime = 0.0
    ptime_start = time.clock()
    TCS = loadTestSuite(input_file)

    P = [0]

    iteration, total = 0, float(len(TCS))
    while len(TCS) > 0:
        iteration += 1
        if iteration % 100 == 0:
            sys.stdout.write("  Progress: {}%\r".format(
                round(100*iteration/total, 2)))
            sys.stdout.flush()

        s = select(TCS)
        P.append(s)
        del TCS[s]

    ptime = time.clock() - ptime_start

    return stime, ptime, P[1:]

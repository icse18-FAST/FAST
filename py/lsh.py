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

from collections import defaultdict
from collections import OrderedDict
import itertools

import xxhash


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# SHINGLING

def kShingles(TS, k):
    """INPUT
    (dict)TS: key=tcID, value=(set of entities)
    (int)k: size of k-shingles

    OUTPUT
    (dict)shingles: key=tcID, value=set of k-shingles of test case ID"""
    shingles = OrderedDict()
    for tcID in TS:
        tc = TS[tcID]
        shingle = set()
        for i in xrange(len(tc) - k + 1):
            shingle.add(hash(tc[i:i + k]))
        shingles[tcID] = shingle

    return shingles


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# MINWISEHASHING

def hashFamily(i):
    def hashMember(x):
        return xxhash.xxh64(x, seed=37 * (2 * i + 1)).digest()

    return hashMember


def tcMinhashing(test_case, hash_functions):
    """INPUT
    (pair)test_case: (tcID, set of entities)
    (list(fun))hash_functions: list of hash_functions

    OUTPUT
    (list)tc_signature: list of minhash values (signature)
    """
    n = len(hash_functions)
    tc_ID, tc_shingles = test_case
    # initialized to max_value ('ffffffff') to correctly compute the min
    tc_signature = ["ffffffff" for i in xrange(n)]
    for tc_shingle in tc_shingles:
        for i in xrange(n):
            tc_hash = hash_functions[i](str(tc_shingle))
            if tc_hash < tc_signature[i]:
                tc_signature[i] = tc_hash

    return tc_signature


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# LOCALITY SENSITIVE HASHING (LSH)

def LSHBucket(minhashes, b, r, n):
    """INPUT
    (dict)minhashes: key=minhashes of test cases
    (int)b: number of bands
    (int)r: number of rows
    (int)n: number of hash functions (n = b*r)

    OUTPUT
    (dict(dict))LSHBuckets: key=band, val=dict(key=col_sig, val=set(tc_IDs))"""
    assert(b * r == n)

    # key=band, val=dict(key=col_sig, val=set(tc_IDs))
    bucket = defaultdict(dict)
    i = 0
    while i < n:  # for each band
        bucket[i] = defaultdict(set)  # to catch collisions in each band
        for tc_signature in minhashes:
            tc_ID, signatures = tc_signature
            column = signatures[i:i + r]
            column_signature = hash(str(column))

            bucket[i][column_signature].add(tc_ID)

        i += r  # next band

    return bucket


def LSHCandidates(bucket, signature, b, r, n):
    """INPUT
    (dict)bucket: key=band, val=dict(key=col_sig, val=set(tc_IDs))
    (pair)signature: (0, minhash)
    (int)b: number of bands
    (int)r: number of rows
    (int)n: number of hash functions (n = b*r)

    OUTPUT
    (set)candidates: set of possibly similar test cases"""
    assert(b * r == n)

    candidates = set()

    i = 0
    while i < n:  # for each band
        tc_ID0, minhash = signature
        column = minhash[i:i + r]
        column_signature = hash(str(column))

        for tc_ID in bucket[i][column_signature]:
            candidates.add(tc_ID)

        i += r  # next band

    return candidates


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# JACCARD SIMILARITY/DISTANCE EXACT AND ESTIMATES

def jSimilarity(a, b):
    return float(len(a & b)) / len(a | b)

def jDistance(a, b):
    return 1.0 - jSimilarity(a, b)

def jSimilarityEstimate(s1, s2):
    assert(len(s1) == len(s2))
    return sum([1 for i in xrange(len(s1)) if s1[i] == s2[i]]) / float(len(s1))

def jDistanceEstimate(s1, s2):
    return 1.0 - jSimilarityEstimate(s1, s2)

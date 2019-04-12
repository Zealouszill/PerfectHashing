# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 10:36:27 2019

@author: spencer.stewart

Start for Perfect Hashing

need to know the length of the outside bucket of keys.
So do 2*len(potential_keys)

Marsane prime is 2^p - 1    p = 11111

Have each string convert to it's own binary sequence.

We need to take for floor of the length of the has to know how many bits
it's going to take to hold the number of bits for each letter

chunk size is equal to the ceil(m/(t-1)]
longest thing in the bucket is m bits long
t is the number of bits it takes to write down the size of the number of buckets.
t = ceil(log_2n)
n is the size of the hash table
chunk size is equal to the size of the first hash table, minus one. So if we have
    32 size, you can represent 31 with 11111. Take a bit off, so you have 4 bit chunk size.
    How many 4 bit chunk sizes can fit into the 32 bit size. 8. That's how many chunks you have.

"""


import random
import math
from sympy import nextprime


class PerfectHashDict(object):

    def __init__(self, possible_keys):

        print("this is possible keys", possible_keys)
        self.keys = possible_keys

        # prime number of buckets that is reasonably large
        self.num_buckets = self.chooseNumBuckets(len(possible_keys) * 2)
        print("Number of Buckets: ", self.num_buckets)

        # hash functions will be sequences of numbers that are less than n
        self.chunk_size = self.computeChunkSize(self.num_buckets)
        print("Number of Chunk Sizes: ", self.chunk_size)

        # we need to see how many parameters our hash functions will need
        # i.e., how many chunks are in the largest input
        max_num_chunks = self.computeMaxNumChunks(self.chunk_size, possible_keys)
        # sample an initial hash function
        self.main_hash_function = self.sampleHashFunction(self.num_buckets, max_num_chunks)
        # TODO: optional: you could sample a few hash functions here and pick the one that
        # will minimize the size of the second tier

        # check how many collisons per bucket
        # bucket_contents = self.hash_all(
        #    keys=possible_keys, params=self.main_hash_function,
        #    n=self.num_buckets, chunk_size=self.chunk_size)
        bucket_contents = self.hash_all()

        # list of lists of values (one list per bucket), size of list should be len(collisions[i]) ** 2
        self.values = [None] * self.num_buckets
        self.chunk_sizes = [None] * self.num_buckets
        self.second_tier_hash_functions = [None] * self.num_buckets
        for bucket, in_bucket in enumerate(bucket_contents):
            if not len(in_bucket):
                continue  # don't bother with empty buckets
            # number of sub_buckets in this bucket to be at least the number of items squared
            n_b = self.chooseNumBuckets(len(in_bucket) ** 2)
            # compute chunk size and number of chunks based on number of buckets
            chunk_size = self.computeChunkSize(n_b)
            max_num_chunks_b = self.computeMaxNumChunks(chunk_size, in_bucket)

            # TODO: keep sampling hash functions until we don't have any collisions
            hash_function = self.sampleHashFunction(n_b, max_num_chunks_b)

            # keep track of the chunk sizes and hash function
            self.chunk_sizes[bucket] = chunk_size
            self.second_tier_hash_functions[bucket] = hash_function
            # make space for storing values corresponding with the key (if any)
            # that maps to each bucket
            self.values[bucket] = [None] * n_b

    def getHashIndex(self, key, hashTimes=True):
        b = self.hash(s=key, params=self.main_hash_function, n=self.num_buckets, chunk_size=self.chunk_size)
        if (hashTimes):
            print("Chunk Sizes: ", self.chunk_sizes)
            b_prime = self.hash(
                s=key, params=self.second_tier_hash_functions[b],
                n=len(self.values), chunk_size=self.chunk_sizes[b])
            return self.values[b][b_prime]
        else:
            return b

    def hash_all(self):
        # start off with an empty list for each bucket
        bucket_contents = list([] for _ in range(self.num_buckets))
        for k in self.keys:
            bucket_contents[self.getHashIndex(k, False)].append(k)
        return bucket_contents

    @staticmethod
    def sampleHashFunction(num_buckets, num_chunks):
        return list(random.randint(0, num_buckets) for _ in range(num_chunks))

    @staticmethod
    def chooseNumBuckets(k):
        """returns a prime number that is at k"""
        return nextprime(k - 1)

    @staticmethod
    def computeMaxNumChunks(chunk_size, keys):
        if chunk_size > 0:
            return max(math.ceil(len(PerfectHashDict.sToBits(k)) / chunk_size) for k in keys)
        else:
            return 1

    @staticmethod
    def computeChunkSize(num_buckets):
        # we will need to split the input into chunks of fewer bits than the number
        # needed to store the number 'num_buckets'
        return math.ceil(math.log(num_buckets, 2)) - 1

    @staticmethod
    def sToInt(s):
        """take in a string and return an integer representing the same bits"""
        shift_by = 0
        total = 0
        for b in bytes(s, encoding='utf-8'):
            total += b << shift_by
            shift_by += 8
        return total

    @staticmethod
    def sToBits(s):
        """returns a string represented as a binary string of '0' and '1' characters"""
        return bin(PerfectHashDict.sToInt(s))[2:]

    @staticmethod
    def numBits(s):
        return bin(PerfectHashDict.sToInt(s))[2:]

    @staticmethod
    def chunkstring(string, length):
        return (string[0 + i:length + i] for i in range(0, len(string), length))

    @staticmethod
    def hash(s, params, n, chunk_size):
        """
        hashes the string, s, into the one of n buckets
        using a universal hash family function parameterized
        by 'params'
        args:
            s: string to hash
            params: list of integers each between 0 and n
            n: prime number representing number of buckets
            chunk_size: size (in bits) of the chunks of s
                (the hash function converts s to a binary string
                and, splits it into (at most len(params)) chunks
                of bits [each of size = chunk_size], multiplies
                each chunk value by the corresponding parameter
                and sums the result
        """


        bits = PerfectHashDict.sToBits(s)

        print("Chunk size in the Hashing Method: ", chunk_size)
        # TODO: split bits into small ints according to chunk size

        # chunk_strs = list(chunkstring(bits, chunk_size))
        chunk_strs = PerfectHashDict.chunkstring(bits, chunk_size)

        # convert the chunks into integers
        chunks = list(int(cs, 2) for cs in chunk_strs)
        hashed = 0
        for chunk, param in zip(chunks, params):
            hashed = (hashed + chunk * param) % n
        return hashed

    def __getitem__(self, key):
        """getter d[key]"""
        return self.getHashIndex(key)

    def __setitem__(self, key, value):
        """setter d[key] = value"""
        self.values[self.getHashIndex(key)] = self.getHashIndex(str(value), False)
        return None


def test_perfect_hash():
    # PerfectHashDict is the goal of this lab
    d = PerfectHashDict(['this', 'that'])
    # constructor initializes empty dictionary

    assert d['this'] is None
    assert d['that'] is None
    # associate values with keys
    d['this'] = 78
    d['that'] = 'some other value'
    # make sure we get the right values
    assert d['this'] == 78
    assert d['that'] == 'some other value'

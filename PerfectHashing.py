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



"""

import math

mersenne_primes = [3, 7, 31] # cont this

def sToInt(s):
    
    """
    Take in a string and return an integer representing the same bits
    """
    shift_by = 0
    total = 0
    for b in bytes(s, encoding = 'utf=8'):
        # print(b)
        total += b << shift_by
        shift_by += 8
        
    return total


def sToBits(s):
    return bin(sToInt(s))[2:]

def test_sToInt():
    

class PerfectHashDict(object):
    
    def __init__(self, possible_keys):
        
        self.possible_keys = possible_keys
        self.num_buckets = min(p for p in mersenne_primes if p >= len(possible_keys) * 2)
        self.chunk_size = math.log(self.num_buckets, 2)
        self.max_num_chunks = max(math.ceil(len(sToBits(k))/self.chunk_size) for key in possible_keys)
        self.hash_function = list(rand(0, self.num_buckets) for _ in range(self.max_num_chunks)) # Change rand function to be what we think it should be
        
        # list of lists of ints representing the list of 2nd level hash functions
        self.second_tier_hash_function = []
        
        # list of lists of items(one list per bucket)
        self.items
        
    def hash1(s):
        bits = sToBits(s)
        # split into small ints according to chunk size
        chunks = []
        hashed = 0
        for chunk, param in zip(chunks, self.hash_function):
            hashed = (hashed + chunk * param) % self.num_buckets
        return hashed

    # getter at d[key]
    def __getitem__(self, key):
        pass

    
    # setter at d[key] = value
    def __setitem__(self, key, value):
        pass


def test_perfect_hash():
    
    # PerfectHashDict is the goal of this lab
    d = PerfectHashDict(['this', 'that'])
    
    # constructor initializes empty dictionary
    # (values are all None)
    assert d['this'] is None
    assert d['that'] is None
    # associate values with keys
    d['this'] = 78
    d['that'] = 'some other value'
    # make sure we get the right values
    assert d['this'] == 78
    assert d['that'] == 'some other value'
    
    
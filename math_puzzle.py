#! /usr/bin/python3

import random

def create_random_int(max : int=15):
    return random.randint(-1 * max,max)

def create_random_operator():
    return random.choice(['+','-'])

# BUG: The ordering of rand_op and new_val is wrong, look at trying to implement 'else' case to see this

def create_puzzle(val=0,length=4,st=''):
    if length > 0:
        rand_int = create_random_int()
        rand_op = create_random_operator()
        new_val = val+rand_int if rand_op == '+' else val-rand_int
        return create_puzzle(val=new_val, length=length-1, st=st + ' ' + str(rand_int) + ' ' + rand_op)
    else:
        rand_int = create_random_int()
        return(val, st + ' ' + str(rand_int))
#! /usr/bin/python3

import random

def create_random_int(max : int=7):
    x = random.randint(-max,max)
    if x == 0:
        x = create_random_int()
    return(x)

ops = ['*','%','+','-']
def create_random_operator():
    return random.choice(ops)

def math_solve(pz):
    for op in ops:
        print(op)
        for i in range(0, len(pz)):
            if pz[i] == op or (op == '+' and pz[i] == '-'): # op - special case handles subtraction not being commutative
                new_val = 0
                prev = int(pz[i-1])
                post = int(pz[i+1])
                if pz[i] == '*':
                    new_val = str(prev * post)
                elif pz[i] == '%':
                    new_val = str(prev % post)
                elif pz[i] == '+':
                    new_val = str(prev + post)
                elif pz[i] == '-':
                    new_val = str(prev - post)
                del(pz[i+1])
                del(pz[i])
                del(pz[i-1])
                pz.insert(i-1, new_val)
                #DEBUG
                s=''
                for s1 in range(0,len(pz)):
                    s+= pz[s1]+' '
                print(s)
                #ENDDEBUG
                return(math_solve(pz))
            elif pz[i] not in ops: # digit
                if len(pz) == 1:
                    return pz[i] # returns solved value


def puzzle():
    pz = create_puzzle()
    return(math_solve(pz.split()), pz)
    
    




MAX_L = 4
def create_puzzle(length=MAX_L,st=''):
    rand_int = create_random_int()
    rand_op = create_random_operator()
    new_st = ''

    # clean up expression syntax
    if rand_op == '-':  
        if rand_int < 0:    # change '- -n' to '+ n'
            rand_int = abs(rand_int)
            rand_op = '+'
    if rand_op == '+':  
        if rand_int < 0:    # change '+ -n' to '- n'
            rand_int = abs(rand_int)
            rand_op = '-'
    if rand_op == '%':
        if rand_int < 0:    # change '% -n' to '% n'
            rand_int = abs(rand_int)
    
    # create string with operator before digit at each step
    if length == 0: # last digit of expression
        new_st = st + ' ' + rand_op + ' ' + str(rand_int)
        # return string
        return new_st
    elif length == MAX_L: # first digit of expression
        new_st = st + '-' + str(rand_int) if rand_op == '-' else st+str(rand_int)
    else:
        new_st = st + ' ' + rand_op + ' ' + str(rand_int)
    return(create_puzzle(length-1, new_st))
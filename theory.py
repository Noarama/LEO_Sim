from functools import lru_cache
from decimal import Decimal, getcontext

getcontext().prec = 50

def one_d_prob(n,d,p):
    return (p**d) + (p**(n-d)) - (p**n)


@lru_cache(maxsize=None)
def theta(x, flag, p_str):
    p = Decimal(p_str)
    one = Decimal(1)

    if (x == 0 and flag == 0) or (x == 1 and flag == 2):
        return Decimal(0)

    elif (x == 1 and flag == 4):
        return p

    prev = theta(x - 1, flag, p_str)
    return p * (p + (one - p) * prev)


@lru_cache(maxsize=None)
def ladder_connectivity(x, p_str):
    p = Decimal(p_str)
    one = Decimal(1)

    if x == 0:
        return p

    px = p ** x
    return p * (px + ladder_connectivity(x - 1, p_str) - px * theta(x, 0, p_str))


def case_one(ccw_x, cw_x, p):
    """
    Case 1: S and D are disconnected (ladder ends do not touch).
    This function returns the two probabilities of ladder connectivity
    from S in counterclockwise and clockwise directions.
    """

    # Convert p to string for safe Decimal use with @lru_cache
    p_str = str(p)

    if ccw_x > 1:
        ccw_prob = (Decimal(p_str) ** 2) * ladder_connectivity(ccw_x - 2, p_str)
    else:
        ccw_prob = Decimal(0)

    if cw_x > 1:
        cw_prob = (Decimal(p_str) ** 2) * ladder_connectivity(cw_x - 2, p_str)
    else:
        cw_prob = Decimal(0)

    return ccw_prob, cw_prob



# @lru_cache(maxsize=None)
# def ladder_connectivity(x,p):
#     if x == 0:
#         return p

#     return p*((p**x) + ladder_connectivity(x-1, p) - (p**x) * theta(p, x, 0))

# @lru_cache(maxsize=None)
# def theta(p,x, flag):
#     ''' This function calculates theta which is part of the theoretical equations. 
#     This function uses:
#     p - The bond probability, 
#     x - the current size, 
#     flag - a flag to indicate which case we are in, 
#     small - a variable that holds a smaller case. This is used to make the recursion less deep.
#     small_x - The size of the small case we already have. 

#     For clarity, we are trying to use previously found cases to make the recursion less deep by using previously 
#     obtained cases. If we do not have a case already obtained, the value of small and small_x is set to -1. If we do have
#     a previously obtained case, small will hold its value and small_x will hold its size. 
#     '''
#     # These are the base cases, depending on the case we are handeling
#     if flag == 2 and x == 1:
#         return 0

#     if flag == 4 and x == 1:
#         return p

#     if flag == 0 and x == 0:
#         return 0

#     # # This if block is to shorten the running time
#     # if small != -1 and x == small_x:
#     #     return small

#     # This is the recursion itself 
#     return (p* (p + (1-p)*theta(p,x-1, flag)))



# def case_one(CCW_x, CW_x, p):
#     ''' This function is responsible for calculating the probability of the two ladders under case one: S and D disconnected.
#     This function is recursive and it uses:
#     CCW_x - The size of the counter-clockwise direction ladder,
#     CW_x - the size of the clockwise direction ladder,
#     p - the bond probability.
#     '''

#     CCW = 0 
#     CW = 0

#     if CCW_x > 1:
#         CCW = (p**2) * ladder_connectivity(CCW_x - 2, p)
    
#     if CW_x > 1:
#         CW = (p**2) * ladder_connectivity(CW_x - 2, p)


#     return CCW, CW 



def case_two_three(CCW_x, CW_x, p, CCW_one, CW_one):
    ''' This function is responsible for calculating the probability of the two ladders under case two and three: one of S and D is disconnected. 
    Thos function is uses:
    CCW_x - The size of the counter-clockwise direction ladder,
    CW_x - the size of the clockwise direction ladder,
    p - the bond probability,
    CCW_one - the value of CCW in case 1,
    CW_one - the value of CW in case 1.
    '''
    p_str = str(p)
    CW = Decimal(p_str)
    CCW = Decimal(p_str)
    

    if CCW_x > 1 and CW_x > 1:
        CCW = (Decimal(p_str)**CCW_x) + CCW_one - (Decimal(p_str)**CCW_x)*theta(CCW_x, 2, p_str)
        CW = (Decimal(p_str)**CW_x) + CW_one - (Decimal(p_str)**CW_x)*theta(CW_x, 2, p_str)

    return CCW, CW



def case_four(CCW_x, CW_x, p, CCW_two, CW_two):
    ''' This function is responsible for calculating the probability of the two ladders under case four: S and D are connected. 
    Thos function is uses:
    CCW_x - The size of the counter-clockwise direction ladder,
    CW_x - the size of the clockwise direction ladder,
    p - the bond probability,
    CCW_two - the value of CCW in case 2,
    CW_two - the value of CW in case 2.
    '''
    p_str = str(p)
    CCW = 2*Decimal(p_str) - (Decimal(p_str)**2)
    CW = 2*Decimal(p_str) - (Decimal(p_str)**2)

    if CCW_x > 1 and CW_x > 1:

        CCW = (Decimal(p_str)**CCW_x) + CCW_two - (Decimal(p_str)**CCW_x)*theta(CCW_x, 4, p_str)
        CW = (Decimal(p_str)**CW_x) + CW_two - (Decimal(p_str)**CW_x)*theta(CW_x, 4, p_str)

    
    return CCW, CW



def two_d_prob(n,d,p):

    CCW_x = d 
    CW_x = n - d 
    p_str = str(p)
    one = Decimal(1)

    CCW_one, CW_one = case_one(CCW_x, CW_x, p)
    CCW_two, CW_two = case_two_three(CCW_x, CW_x, p, CCW_one, CW_one)
    CCW_four, CW_four = case_four(CCW_x, CW_x, p, CCW_two, CW_two)


    return ((one-Decimal(p_str))**2)*(CW_one+CCW_one - CW_one*CCW_one) + 2*(Decimal(p_str)*(one-Decimal(p_str)))*(CW_two+ CCW_two - CW_two*CCW_two) + (Decimal(p_str)**2)*(CW_four + CCW_four - CW_four * CCW_four) 
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
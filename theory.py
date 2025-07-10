def one_d_prob(n,d,p):
    return (p**d) + (p**(n-d)) - (p**n)



def ladder_connectivity(x,p):
    if x == 0:
        return p

    return p*((p**x) + ladder_connectivity(x-1, p) - (p**x) * theta(p, x, 0, -1,-1))


def theta(p,x, flag, small, small_x):
    ''' This function calculates theta which is part of the theoretical equations. 
    This function uses:
    p - The bond probability, 
    x - the current size, 
    flag - a flag to indicate which case we are in, 
    small - a variable that holds a smaller case. This is used to make the recursion less deep.
    small_x - The size of the small case we already have. 

    For clarity, we are trying to use previously found cases to make the recursion less deep by using previously 
    obtained cases. If we do not have a case already obtained, the value of small and small_x is set to -1. If we do have
    a previously obtained case, small will hold its value and small_x will hold its size. 
    '''

    # These are the base cases, depending on the case we are handeling
    if flag == 2 and x == 1:
        return 0

    if flag == 4 and x == 1:
        return p

    if flag == 0 and x == 0:
        return 0

    # This if block is to shorten the running time
    if small != -1 and x == small_x:
        return small

    # This is the recursion itself 
    return (p* (p + (1-p)*theta(p,x-1, flag, small, small_x)))



def case_one(CCW_x, CW_x, p):
    ''' This function is responsible for calculating the probability of the two ladders under case one: S and D disconnected.
    This function is recursive and it uses:
    CCW_x - The size of the counter-clockwise direction ladder,
    CW_x - the size of the clockwise direction ladder,
    p - the bond probability.
    '''

    CCW = 0 
    CW = 0

    if CCW_x > 1:
        CCW = (p**2) * ladder_connectivity(CCW_x - 2, p)
    
    if CW_x > 1:
        CW = (p**2) * ladder_connectivity(CW_x - 2, p)


    return CCW, CW 



def case_two_three(CCW_x, CW_x, p, CCW_one, CW_one):
    ''' This function is responsible for calculating the probability of the two ladders under case two and three: one of S and D is disconnected. 
    Thos function is uses:
    CCW_x - The size of the counter-clockwise direction ladder,
    CW_x - the size of the clockwise direction ladder,
    p - the bond probability,
    CCW_one - the value of CCW in case 1,
    CW_one - the value of CW in case 1.
    '''
    CW = p
    CCW = p

    if CCW_x > 1 and CW_x > 1:

        if CCW_x <= CW_x:

            if CCW_x != 1:
                CCW = (p**CCW_x) + CCW_one - (p**CCW_x)*theta(p, CCW_x, 2, -1,-1)

            if CW_x != 1:
                CW = (p**CW_x) + CW_one - (p**CW_x)*theta(p, CW_x, 2, CCW, CCW_x)
        
        else:

            if CW_x != 1:
                CW = (p**CW_x) + CW_one - (p**CW_x)*theta(p, CW_x, 2, -1,-1)

            if CCW_x != 1:
                CCW = (p**CCW_x) + CCW_one - (p**CCW_x)*theta(p, CCW_x, 2, CW, CW_x)


    else: 
        if CW_x > 1:
            CW = (p**CW_x) + CW_one - (p**CW_x)*theta(p, CW_x, 2, -1,-1)

        if CCW_x > 1:
            CCW = (p**CCW_x) + CCW_one - (p**CCW_x)*theta(p, CCW_x, 2, -1, -1)
        

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
    CCW = 2*p - (p**2)
    CW = 2*p - (p**2)
    if CCW_x > 1 and CW_x > 1:
        # If both are not 1
        if CCW_x <= CW_x:

            if CCW_x != 1:
                CCW = (p**CCW_x) + CCW_two - (p**CCW_x)*theta(p, CCW_x, 4, -1,-1)

            if CW_x != 1:
                CW = (p**CW_x) + CW_two - (p**CW_x)*theta(p, CW_x, 4, CCW, CCW_x)
        
        else:

            if CW_x != 1:
                CW = (p**CW_x) + CW_two - (p**CW_x)*theta(p, CW_x, 4, -1,-1)

            if CCW_x != 1:
                CCW = (p**CCW_x) + CCW_two - (p**CCW_x)*theta(p, CCW_x, 4, CW, CW_x)


    else: 
        # If one is not 1
        if CW_x > 1:
            CW = (p**CW_x) + CW_two - (p**CW_x)*theta(p, CW_x, 4, -1,-1)

        if CCW_x > 1:
            CCW = (p**CCW_x) + CCW_two - (p**CCW_x)*theta(p, CCW_x, 4, -1, -1)
    
    return CCW, CW



def two_d_prob(n,d,p):

    CCW_x = d 
    CW_x = n - d 
    # print("sizes:" , CW_x, CCW_x)

    CCW_one, CW_one = case_one(CCW_x, CW_x, p)
    CCW_two, CW_two = case_two_three(CCW_x, CW_x, p, CCW_one, CW_one)
    CCW_four, CW_four = case_four(CCW_x, CW_x, p, CCW_two, CW_two)

    if CCW_x == 0:
        CCW_one = 0
        CCW_two = 0
        CCW_four = 0
    
    # if CW_x == 0:
    #     CW_one = 1
    #     CW_two = 1
    #     CW_four = 1
    
    # print("Values:")
    # print(CW_one, CCW_one)
    # print(CW_two, CCW_two)
    # print(CW_four, CCW_four)

    # return (CW_one + CCW_one - CW_one * CCW_one)

    return ((1-p)**2)*(CW_one+CCW_one - CW_one*CCW_one) + 2*(p*(1-p))*(CW_two+ CCW_two - CW_two*CCW_two) + (p**2)*(CW_four + CCW_four - CW_four * CCW_four)
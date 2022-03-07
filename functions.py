# NYU Tandon School of Engineering
# FRE-GY 6831 Computational Finance Laboratory (Python) - Spring 2022
# Project: US Treasury Bond Analytics
# Part One - functions.py
# Author: Michael Qu (LQ2038)

def getPrice(N: int, r: float, c: float) -> float:
    """Calculates the price of a bond as a percentage of its face value.

    See Slide 11. (Bond Pricing and YTM)

    :param N: number of coupon periods
    :param r: periodic discounting rate
    :param c: periodic coupon
    """
    r /= 100
    c /= 100
    M = 0
    for i in range(1,N+1):
        M += c/((1+r)**i)

    M += 1/((1+r)**N)
    return M


def getPV01(N: int, P: float, r: float, c: float) -> float:
    """Calculates the PV01 of a bond.

    See Slide 25. (Duration and PVBP)

    :param N: number of payment periods
    :param P: bond price as a percentage of its face value
    :param r: periodic discounting rate (in percentage)
    :param c: periodic coupon (in percentage)
    """
    dP = dPdr(N, r, c)
    return dP*P*(-0.0001)


def getYTM(N: int, P: float, c: float) -> float:
    """Calculates the Yield To Maturity of a bond for a given price using Newton's method
    i.e. to find r s.t. PV(r) = P

    See Slide 14. (Bond Pricing and YTM)

    :param N: number of payment periods
    :param P: bond price as a percentage of its face value (normally slightly larger than 1, e.g, 10x%)
    :param c: periodic coupon (in percentage)
    """
    P /= 100
    r = 0
    while True:
        dr = (getPrice(N, r, c) - P)/dPdr(N, r, c)
        #print(dr)
        r -= dr
        if abs(dr) < 0.0001:
            break
        
    return r
    

def getModDur(N: int, P: float, y: float, c: float) -> float:
    """Calculates the modified duration of a bond.

    See Slide 25. (Duration and PVBP)

    :param N: number of payment periods
    :param P: bond price as a percentage of its face value
    :param y: yield to maturity (in percentage)
    :param c: periodic coupon (in percentage)
    """
    y /= 100
    c /= 100
    CashFlow = []
    DiscountFactor = []
    tPVCF = []
    PVCF = []
    n = 1     # Assume annual coupon (2 for semi-annual coupon)
    r = y/n
    c = c/n
    for t in range(1, N+1):
        DiscountFactor.append(1/(1+r)**t)
        if t<N:
            CashFlow.append(P*c)
        else:   # t = N
            CashFlow.append(P*c + P)
        
        PVCF.append(CashFlow[-1]*DiscountFactor[-1])
        tPVCF.append(t*PVCF[-1])

    MacaulayDur = sum(tPVCF)/sum(PVCF)
    return MacaulayDur/(1+r)


def parseQuote(quoteString: str) -> float:
    """Calculates a bond price as a percentage of par.

    See Slide 16. (Bond Pricing and YTM)

    :param quoteString: a bond quote in string form
    with format "handle-32nds+++++"
    where "handle" (big number) is the integer portion of the percentage
    "32nds" is the number representing how many 1/32 in the percentage
    Additional "+"s: first '+' represents 1/64, the 2nd '+' represents 1/128, ...
    """

    parts = quoteString.split("-")
    # If there is only integer portion
    if len(parts) == 1:
        return float(parts[0])
    
    # If there is one "-" separating the "big figure" and the fraction portion
    if len(parts) == 2:
        initial = float(parts[0])    # Capture the "big figure"
        pls = parts[1].split("+")    # e.g. if parts = "24++", then pls = ['24' '' '']
        initial += int(pls[0]) / 32  # Include the 32nds

        if len(pls) == 1:            # There is no "+" in the input
            return initial
        
        denom = 64
        for _ in range(1, len(pls)):
            initial += 1 / denom
            denom *= 2
        return initial
        
    raise Exception("Invalid input of bond quote")


def dPdr(N: int, r: float, c: float) -> float:
    '''Calculate the derivative of price at a given rate analytically

    See Slide 25. (Duration and PVBP)

    :param N: number of payment periods
    :param r: periodic discounting rate (in percentage)
    :param c: periodic coupon (in percentage)
    '''
    r /= 100
    c /= 100
    sum = 0
    for i in range(1, N+1):
        discountFactor = 1/(1+r)**i
        sum += i*c*discountFactor
    
    return -(sum + N*discountFactor)/(1+r)

# NYU Tandon School of Engineering
# FRE-GY 6831 Computational Finance Laboratory (Python) - Spring 2022
# Project: US Treasury Bond Analytics
# Author: Michael Qu (LQ2038)

from calendar import c
import datetime as dt
from logging import raiseExceptions

class USTreasurySecurity:
    def __init__(
          self,
          quoteString: str,
          N: int,
          a: float,
          tradeDate: dt.date,
          prevCouponDate: dt.date,
          nextCouponDate: dt.date,
          holidayCalendar: list,
    ):
        # Quoted price from market, e.g. "100-24" -> 100.75
        #self.__quoteString = quoteString
        self.__price = self.parseQuote(quoteString)
        # Number of payments. If N > 1, there is (N-1) full periods and another z/x period      
        self.__N = N
        # Convert annulized coupon to semi-annual periodic coupon. e.g. 0.06 -> 0.03
        self.__c = a/2

        # Calendar calculation, accrued ratio for the first payment = z/x
        self.__holidays = set()
        for day in holidayCalendar:
            self.__holidays.add(dt.datetime.strptime(day, "%d-%m-%Y").date())

        self.__settlementDate = self.getSettlementDate(tradeDate)
        self.__prevCouponDate = prevCouponDate
        self.__nextCouponDate = nextCouponDate
        #self.__x = 180

        # Use iterative method to calculate yield to maturity
        self.__y = self.__getYTM()
    
    #----------------------------------------------------------------------------------
    # Interface
    @property
    def N(self):
        return self.__N

    @property
    def c(self):
        return self.__c

    @property
    def settlementDate(self):
        return self.__settlementDate

    @property
    def prevCouponDate(self):
        return self.__prevCouponDate

    @property
    def nextCouponDate(self):
        return self.__nextCouponDate
    
    #----------------------------------------------------------------------------------
    # Essential Functions
    def __getPrice(self, y: float) -> float:
        # Calculates the (dirty) price of a bond as a percentage of its face value.
        P = 0
        r = y/2
        z = self.__nextCouponDate - self.__settlementDate
        z = z.days
        x = self.__nextCouponDate - self.__prevCouponDate
        x = x.days
        accruedRatio = z/x
        if self.__N == 1:
            # See Slide 19 (Bond Pricing and YTM)
            P = (1 + self.__c) / (1 + r * accruedRatio)
        else:
            # See Slide 18 (Bond Pricing and YTM)
            P = 0
            for t in range(0, self.__N):
                discountFactor = 1/(1 + r)**(t + accruedRatio)
                if t < self.__N - 1:    # Only coupon is returned
                    cashFlow = self.__c
                else:      # t = N - 1, the last coupon and the principle are returned
                    cashFlow = self.__c + 1
                
                P += cashFlow * discountFactor
    
        return P

    def __dPdy(self, y: float) -> float:
        # Calculate the derivative of (dirty) price at a given rate analytically
        dPdr = 0
        r = y/2
        z = self.__nextCouponDate - self.__settlementDate
        z = z.days
        x = self.__nextCouponDate - self.__prevCouponDate
        x = x.days
        accruedRatio = z/x
        if self.__N == 1:
            # Take derivative of formula in Slide 19 (Bond Pricing and YTM)
            dPdr = - (1 + self.__c) * accruedRatio / (1 + r * accruedRatio)**2
            
        else:
            # Take derivative of formula in Slide 18 (Bond Pricing and YTM)
            for t in range(0, self.__N):
                discountFactor = 1/(1 + r)**(t + accruedRatio)
                if t < self.__N - 1:    # Only coupon is returned
                    cashFlow = self.__c
                else:      # t = N - 1, the last coupon and the principle are returned
                    cashFlow = self.__c + 1
                
                dPdr += cashFlow * (-t-accruedRatio) * discountFactor / (1+r)
                
        dPdy = dPdr/2
        return dPdy

    def getPV01(self) -> float:
        #return self.__dPdy(self.__y)*(-0.0001)
        #return self.__dPdy(self.__y)*(-1)
        return self.getDirtyPrice()*self.getModDur()*0.01

    def __getYTM(self):
        # Calculates the Yield To Maturity of a bond for a given price using Newton's method
        # i.e. to find r s.t. PV(r) = P
        # See Slide 14. (Bond Pricing and YTM)
        tol = 0.0001
        relativePrice = self.__price/100
        yGuess = 0
        while True:
            dy = (self.__getPrice(yGuess) - relativePrice)/self.__dPdy(yGuess)
            yGuess -= dy
            if abs(dy) < tol:
                break
        
        return yGuess
    
    def getYTM(self) -> float:
        return self.__y

    def getModDur(self) -> float:
        return -self.__dPdy(self.__y)/(self.__price/100)
        
        '''
        r = self.__y/2
        z = self.__nextCouponDate - self.__settlementDate
        z = z.days
        x = self.__nextCouponDate - self.__prevCouponDate
        x = x.days
        accruedRatio = z/x

        
        if self.__N == 1:
            # See Slide 19 (Bond Pricing and YTM)
            P = (1 + self.__c) / (1 + r * accruedRatio)
            tp = accruedRatio * P
        else:
            # See Slide 18 (Bond Pricing and YTM)
            P = 0
            tP = 0
            for t in range(0, self.__N):
                discountFactor = 1/(1 + r)**(t + accruedRatio)
                if t < self.__N - 1:    # Only coupon is returned
                    cashFlow = self.__c
                else:      # t = N - 1, the last coupon and the principle are returned
                    cashFlow = self.__c + 1
                
                P += cashFlow * discountFactor
                tP += (t + accruedRatio) * cashFlow * discountFactor
            
        dur = tP/P
        modDur = dur/(1+r)/2

        return modDur
        '''


    def getDirtyPrice(self) -> float:
        z = self.__settlementDate - self.__prevCouponDate
        z = z.days
        x = self.__nextCouponDate - self.__prevCouponDate
        x = x.days
        accruedRatio = z/x
        accrued = self.__c*100*accruedRatio
        return self.getCleanPrice() + accrued
    
    def getCleanPrice(self) -> float:
        # Clean price is the price quoted from the market
        return self.__price

    #---------------------------------------------------------------------------------------------------
    # Helper Functions
    

    def getSettlementDate(self, tradeDate: dt.date) -> dt.date:
        # Settlement date is the next business day after the trade date
        settlementDate = tradeDate + dt.timedelta(days=1)
        while (settlementDate.weekday()==5 or settlementDate.weekday()==6 or settlementDate in self.__holidays):
            settlementDate += dt.timedelta(days=1)
            
        return settlementDate


    def parseQuote(self, quoteString: str) -> float:
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
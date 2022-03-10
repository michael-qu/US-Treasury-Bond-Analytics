import datetime as dt

from fre6831 import USTreasurySecurity

'''
# any imports you'd like to test
from fre6831.functions import getPrice as testGetPrice
from fre6831.functions import getPV01 as testGetPV01

# helper starter asserts
from fre6831.testing import ASSERT_EQ
from fre6831.testing import ASSERT_SAME
from fre6831.testing import ASSERT_CLOSE
# make your own?  ASSERT_NEQ?  ASSERT_CONTAINS? etc.


# no other imports should be used here


def test_function():
    """Example (Optional) tests..."""
    # result = testGetPrice(...)

    ASSERT_EQ("same value", 10, 10, "int vs. int")
    ASSERT_EQ("same value", 10, 10.0, "int vs. float")

    x = 10
    y = 10
    ASSERT_SAME("same object ref", x, y, "x and y should point to "
                                         "the same object")
    x += 5
    ASSERT_SAME("same object ref", x, y, "x and y are no longer the "
                                         "same object")

    zzz = 1.2344
    www = 1.0
    ASSERT_CLOSE("approximate closeness", zzz, www, "are not close")
    www = 1.2344000000001
    ASSERT_CLOSE("approximate closeness", zzz, www, "within tolerance")
'''    
'''
def readHolidays(path: str) -> set:
        with open(path) as f:
            holidaySet = set()
            for line in f.readlines():
                line = line.strip()
                #holidaySet.add(dt.datetime.strptime(line, "%d-%m-%Y").date())
                holidaySet.add(line)

        return holidaySet
'''

def test_class():
    #path = "holidays.txt"
    #holidays = readHolidays(path)
    #holidays = list(holidays)
    #holidays = ['01-01-2021', '01-15-2021', '02-19-2021', '05-28-2021', '07-04-2021', '09-03-2021', '10-08-2021', '11-12-2021', '11-22-2021', '12-25-2021']
    holidays = ['01-01-2007', '15-01-2007', '19-02-2007', '28-05-2007', '04-07-2007', '03-09-2007', 
                '08-10-2007', '12-11-2007', '22-11-2007', '25-12-2007']
    '''
    a = USTreasurySecurity("100-24", 4, 0.06,
                           dt.date(2007, 1, 12), dt.date(2007, 1, 16),
                           dt.date(2007, 7, 16), holidays)
    '''
    sec = []
    
    sec.append(USTreasurySecurity("99.714939353374", 4, 0.04, dt.date(2007, 8, 30),
                        dt.date(2007, 8, 31), dt.date(2008, 2, 29), holidays))
    sec.append(USTreasurySecurity("100.83075469629", 6, 0.045, dt.date(2007, 8, 30),
                        dt.date(2007, 5, 15), dt.date(2007, 11, 15), holidays))
    # 99+12.25/32 = 99.3828125
    sec.append(USTreasurySecurity("99.3828125", 10, 0.04125, dt.date(2007, 8, 30),
                        dt.date(2007, 8, 31), dt.date(2008, 2, 29), holidays))
    # 101+19.5/32 = 101.609375
    sec.append(USTreasurySecurity("101.609375", 20, 0.0475, dt.date(2007, 8, 30),
                        dt.date(2007, 8, 15), dt.date(2008, 2, 15), holidays))
    
    sec.append(USTreasurySecurity("102.50001753443", 60, 0.05, dt.date(2007, 8, 30),
                        dt.date(2007, 5, 15), dt.date(2007, 11, 15), holidays))
    

    for ind, bond in enumerate(sec):
        print("Bond {i}".format(i = ind + 1))
        #print("Settlement Date: {date}".format(date = bond.settlementDate))
        #print("Days between prev and next coupon dates: {x}".format(x = bond.nextCouponDate - bond.prevCouponDate))
        #print("Days between prev coupon date and settlement day: {z}".format(z = bond.settlementDate - bond.prevCouponDate))
        print("YTM: {y}".format(y = bond.getYTM()))
        print("PV01: {PV01}".format(PV01 = bond.getPV01()))
        print("Modified Duration: {modDur}".format(modDur = bond.getModDur()))
        print("Dirty Price: {d}".format(d = bond.getDirtyPrice()))
        print("Clean Price: {c}".format(c = bond.getCleanPrice()))

if __name__ == "__main__":
    #test_function()
    test_class()

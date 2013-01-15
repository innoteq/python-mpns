import requests

# MPNS overview: http://msdn.microsoft.com/en-us/library/ff402558%28v=vs.92%29.aspx
# Protocol specification: http://msdn.microsoft.com/en-us/library/hh202945%28v=vs.92%29.aspx
# Error codes: http://msdn.microsoft.com/en-us/library/ff941100%28v=VS.92%29.aspx

# Also see Authenticated Web Service: http://msdn.microsoft.com/en-us/library/ff941099%28v=vs.92%29.aspx

class MPNSBase(object):
    DELAY_IMMEDIATE = None
    DELAY_450S = None
    DELAY_900S = None

class MPNSTile(MPNSBase):
    DELAY_IMMEDIATE = 1
    DELAY_450S = 11
    DELAY_900S = 21


class MPNSToast(MPNSBase):
    DELAY_IMMEDIATE = 2
    DELAY_450S = 12
    DELAY_900S = 22


class MPNSRaw(MPNSBase):
    DELAY_IMMEDIATE = 3
    DELAY_450S = 13
    DELAY_900S = 23

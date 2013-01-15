import requests

# MPNS overview: http://msdn.microsoft.com/en-us/library/ff402558%28v=vs.92%29.aspx
# Protocol specification: http://msdn.microsoft.com/en-us/library/hh202945%28v=vs.92%29.aspx
# Error codes: http://msdn.microsoft.com/en-us/library/ff941100%28v=VS.92%29.aspx

# Also see Authenticated Web Service: http://msdn.microsoft.com/en-us/library/ff941099%28v=vs.92%29.aspx

class MPNSBase(object):
    DELAY_IMMEDIATE = None
    DELAY_450S = None
    DELAY_900S = None

    def __init__(self, delay=None):
        self.delay = delay or self.DELAY_IMMEDIATE
        self.headers = {
            'Content-Type': 'text/xml',
            'Accept': 'application/*',
            'X-NotificationClass': str(self.delay),
            }

    def set_target(self, target):
        self.headers['X-WindowsPhone-Target'] = target


class MPNSTile(MPNSBase):
    DELAY_IMMEDIATE = 1
    DELAY_450S = 11
    DELAY_900S = 21

    def __init__(self, *args, **kwargs):
        super(MPNSTile, self).__init__(*args, **kwargs)
        self.set_target('tile') # TODO: flip tile


class MPNSToast(MPNSBase):
    DELAY_IMMEDIATE = 2
    DELAY_450S = 12
    DELAY_900S = 22

    def __init__(self, *args, **kwargs):
        super(MPNSToast, self).__init__(*args, **kwargs)
        self.set_target('token')


class MPNSRaw(MPNSBase):
    DELAY_IMMEDIATE = 3
    DELAY_450S = 13
    DELAY_900S = 23

    def __init__(self, *args, **kwargs):
        super(MPNSRaw, self).__init__(*args, **kwargs)
        self.set_target('raw')

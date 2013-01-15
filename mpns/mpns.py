import requests

# MPNS overview: http://msdn.microsoft.com/en-us/library/ff402558%28v=vs.92%29.aspx
# Protocol specification: http://msdn.microsoft.com/en-us/library/hh202945%28v=vs.92%29.aspx
# Error codes: http://msdn.microsoft.com/en-us/library/ff941100%28v=VS.92%29.aspx

# Also see Authenticated Web Service: http://msdn.microsoft.com/en-us/library/ff941099%28v=vs.92%29.aspx

class MPNSBase(object):
    DELAY_IMMEDIATE = None
    DELAY_450S = None
    DELAY_900S = None

    HEADER_NOTIFICATION_CLASS = 'X-NotificationClass'
    HEADER_TARGET = 'X-WindowsPhone-Target'
    HEADER_MESSAGE_ID = 'X-MessageID'
    HEADER_CALLBACK_URI = 'X-CallbackURI'

    def __init__(self, delay=None):
        self.delay = delay or self.DELAY_IMMEDIATE
        self.headers = {
            'Content-Type': 'text/xml',
            'Accept': 'application/*',
            self.HEADER_NOTIFICATION_CLASS: str(self.delay),
            }

    def set_target(self, target):
        self.headers[self.HEADER_TARGET] = target

    def send(uri, payload, message_id=None, callback_uri=None):
        # reset per-message headers
        for k in (self.HEADER_MESSAGE_ID, self.HEADER_CALLBACK_URI):
            if k in self.headers: self.headers.pop(k)

        # set per-message headers if necessary
        if msgid:
            self.headers[self.HEADER_MESSAGE_ID] = str(msgid) # TODO: validate UUID

        if callback_uri:
            self.headers[self.HEADER_CALLBACK_URI] = str(callback_uri)


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

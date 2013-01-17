python-mpns
===========

Python module for Microsoft Push Notification Service (MPNS) for Windows Phone.

It supports Toast, Tile and Raw notification formats (the latter one is not tested yet).

Usage
-----

    from mpns import MPNSTile, MPNSToast, MPNSRaw

    uri = 'http://db3.notify.live.net/throttledthirdparty/01.00/ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    toast = MPNSToast()
    tile = MPNSTile()

    toast.send(uri, {'text1': 'Hello', 'text2': 'Windows Phone'})
    toast.send(uri, {'text1': 'Tap this message', 'text2': 'To open application'})

    tile.send(uri, {'title': 'Tile title'}


Useful links
------------

MPNS overview:             http://msdn.microsoft.com/en-us/library/ff402558%28v=vs.92%29.aspx

Protocol specification:    http://msdn.microsoft.com/en-us/library/hh202945%28v=vs.92%29.aspx

WP8 enhancements:          http://msdn.microsoft.com/en-us/library/windowsphone/develop/hh202948%28v=vs.105%29.aspx

Error codes:               http://msdn.microsoft.com/en-us/library/ff941100%28v=VS.92%29.aspx

Authenticated Web Service: http://msdn.microsoft.com/en-us/library/ff941099%28v=vs.92%29.aspx


TODO
----

* Support Windows Phone 8 extended tile notifications
* More testing

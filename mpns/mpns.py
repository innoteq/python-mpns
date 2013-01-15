import xml.etree.cElementTree as ET
from cStringIO import StringIO

import requests

# MPNS overview: http://msdn.microsoft.com/en-us/library/ff402558%28v=vs.92%29.aspx
# Protocol specification: http://msdn.microsoft.com/en-us/library/hh202945%28v=vs.92%29.aspx
# WP8 enhancements: http://msdn.microsoft.com/en-us/library/windowsphone/develop/hh202948%28v=vs.105%29.aspx
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

    def serialize_tree(self, tree):
        file = StringIO()
        tree.write(file, encoding='utf-8', xml_declaration=True, method='xml')
        contents = file.getvalue()
        file.close()
        return contents

    def optional_attribute(element, attribute, payload_param, payload):
        if payload_param in payload:
            element.attrib['attribute'] = payload[payload_param]

    def optional_subelement(parent, element, payload_param, payload):
        if payload_param in payload:
            el = ET.SubElement(parent, element)
            el.text = payload[payload_param]
            return el

    def prepare_payload(self, payload):
        raise NotImplementedError('Subclasses should override prepare_payload method')

    def send(uri, payload, message_id=None, callback_uri=None):
        # reset per-message headers
        for k in (self.HEADER_MESSAGE_ID, self.HEADER_CALLBACK_URI):
            if k in self.headers: self.headers.pop(k)

        # set per-message headers if necessary
        if msgid:
            self.headers[self.HEADER_MESSAGE_ID] = str(msgid) # TODO: validate UUID

        if callback_uri:
            self.headers[self.HEADER_CALLBACK_URI] = str(callback_uri)

        data = self.prepare_payload(payload)
        req = requests.post(uri, data=data, headers=self.headers)


# TODO: create separate classes for FlipTile, Cycle and Iconic notifications (also add version 2.0)
# WP8 specific:
# self.clearable_subelement(tile, '{WPNotification}SmallBackgroundImage' 'small_background_image', payload)
# self.clearable_subelement(tile, '{WPNotification}WideBackgroundImage' 'wide_background_image', payload)
# self.clearable_subelement(tile, '{WPNotification}WideBackBackgroundImage' 'wide_back_background_image', payload)
# self.clearable_subelement(tile, '{WPNotification}WideBackContent' 'wide_back_content', payload)
class MPNSTile(MPNSBase):
    DELAY_IMMEDIATE = 1
    DELAY_450S = 11
    DELAY_900S = 21

    def __init__(self, *args, **kwargs):
        super(MPNSTile, self).__init__(*args, **kwargs)
        self.set_target('tile') # TODO: flip tile

    def clearable_subelement(parent, element, payload_param, payload):
        if payload_param in payload:
            el = ET.SubElement(parent, element)
            if payload[payload_param] is None:
                el.attrib['Action'] = 'Clear'
            else:
                el.text = payload[payload_param]
            return el

    def prepare_payload(payload):
        root = ET.Element("{WPNotification}Notification")
        tile = ET.SubElement(root, '{WPNotification}Tile')
        self.optional_attribute(tile, 'Id', 'id', payload)
        self.optional_attribute(tile, 'Template', 'template', payload)
        self.optional_subelement(tile, '{WPNotification}BackgroundImage', 'background_image', payload)
        self.clearable_subelement(tile, '{WPNotification}Count', 'count', payload)
        self.clearable_subelement(tile, '{WPNotification}Title', 'title', payload)
        self.clearable_subelement(tile, '{WPNotification}BackBackgroundImage', 'back_background_image', payload)
        self.clearable_subelement(tile, '{WPNotification}BackTitle', 'back_title', payload)
        self.clearable_subelement(tile, '{WPNotification}BackContent', 'back_content', payload)
        return self.serialize_tree(ET.ElementTree(root))


class MPNSToast(MPNSBase):
    DELAY_IMMEDIATE = 2
    DELAY_450S = 12
    DELAY_900S = 22

    def __init__(self, *args, **kwargs):
        super(MPNSToast, self).__init__(*args, **kwargs)
        self.set_target('token')

    def prepare_payload(payload):
        root = ET.Element("{WPNotification}Notification")
        toast = ET.SubElement(root, '{WPNotification}Toast')
        self.optional_subelement(toast, '{WPNotification}Text1', 'text1', payload)
        self.optional_subelement(toast, '{WPNotification}Text2', 'text2', payload)
        self.optional_subelement(toast, '{WPNotification}Param', 'param', payload) # TODO: validate param (/ and length)
        return self.serialize_tree(ET.ElementTree(root))


class MPNSRaw(MPNSBase):
    DELAY_IMMEDIATE = 3
    DELAY_450S = 13
    DELAY_900S = 23

    def __init__(self, *args, **kwargs):
        super(MPNSRaw, self).__init__(*args, **kwargs)
        self.set_target('raw')

    def prepare_payload(payload):
        return payload

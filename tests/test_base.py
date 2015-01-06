import httpretty
import requests

from mpns import MPNSTile


class Test_Base(object):
    @httpretty.activate
    def test_parse_response_200(self):
        # Mocking response headers
        test_tile_URI = "http://testuri.com/"
        httpretty.register_uri(httpretty.POST,
                               test_tile_URI,
                               content_type='text/json',
                               adding_headers={"x-deviceconnectionstatus": "Test",
                                               "x-notificationstatus": "Test",
                                               "x-subscriptionstatus": "Test",
                                               "x-messageid": "Test"},
                               status=200)

        # Creating MPNS object, posting request and
        # submitting response to parse_response
        test_tile = MPNSTile()
        response = requests.post(test_tile_URI)
        status = test_tile.parse_response(response)

        # Checking status code, error message and ensuring
        # other headers passed without unaltered
        assert status['http_status_code'] == 200
        assert status['device_connection_status'] == 'Test'
        assert status['subscription_status'] == 'Test'
        assert status['notification_status'] == 'Test'
        assert status['message_id'] == 'Test'

    @httpretty.activate
    def test_parse_response_200_queue_full(self):
        # Mocking response headers
        test_tile_URI = "http://testuri.com/"
        httpretty.register_uri(httpretty.POST,
                               test_tile_URI,
                               content_type='text/json',
                               adding_headers={"x-deviceconnectionstatus": "Test",
                                               "x-notificationstatus": "QueueFull",
                                               "x-subscriptionstatus": "Test",
                                               "x-messageid": "Test"},
                               status=200)

        # Creating MPNS object, posting request and
        # submitting response to parse_response
        test_tile = MPNSTile()
        response = requests.post(test_tile_URI)
        status = test_tile.parse_response(response)

        # Checking status code, error message and ensuring
        # other headers passed without unaltered
        assert status['http_status_code'] == 200
        assert status['error'] == 'Queue full, try again later'
        assert status['backoff_seconds'] == 60
        assert status['device_connection_status'] == 'Test'
        assert status['subscription_status'] == 'Test'
        assert status['notification_status'] == 'QueueFull'
        assert status['message_id'] == 'Test'

    @httpretty.activate
    def test_parse_response_400(self):
        # Mocking response headers
        test_tile_URI = "http://testuri.com/"
        httpretty.register_uri(httpretty.POST,
                               test_tile_URI,
                               content_type='text/json',
                               adding_headers={"x-deviceconnectionstatus": "Test",
                                               "x-notificationstatus": "Test",
                                               "x-subscriptionstatus": "Test",
                                               "x-messageid": "Test"},
                               status=400)

        # Creating MPNS object, posting request and
        # submitting response to parse_response
        test_tile = MPNSTile()
        response = requests.post(test_tile_URI)
        status = test_tile.parse_response(response)

        # Checking status code, error message and ensuring
        # other headers passed without unaltered
        assert status['http_status_code'] == 400
        assert status['error'] == 'Bad Request - invalid payload or subscription URI'
        assert status['device_connection_status'] == 'Test'
        assert status['subscription_status'] == 'Test'
        assert status['notification_status'] == 'Test'
        assert status['message_id'] == 'Test'

    @httpretty.activate
    def test_parse_response_401(self):
        # Mocking response headers
        test_tile_URI = "http://testuri.com/"
        httpretty.register_uri(httpretty.POST,
                               test_tile_URI,
                               content_type='text/json',
                               adding_headers={"x-deviceconnectionstatus": "Test",
                                               "x-notificationstatus": "Test",
                                               "x-subscriptionstatus": "Test",
                                               "x-messageid": "Test"},
                               status=401)

        # Creating MPNS object, posting request and
        # submitting response to parse_response
        test_tile = MPNSTile()
        response = requests.post(test_tile_URI)
        status = test_tile.parse_response(response)

        # Checking status code, error message and ensuring
        # other headers passed without unaltered
        assert status['http_status_code'] == 401
        assert status['error'] == 'Unauthorized - invalid token or subscription URI'
        assert status['drop_subscription'] is True
        assert status['device_connection_status'] == 'Test'
        assert status['subscription_status'] == 'Test'
        assert status['notification_status'] == 'Test'
        assert status['message_id'] == 'Test'

    @httpretty.activate
    def test_parse_response_404(self):
        # Mocking response headers
        test_tile_URI = "http://testuri.com/"
        httpretty.register_uri(httpretty.POST,
                               test_tile_URI,
                               content_type='text/json',
                               adding_headers={"x-deviceconnectionstatus": "Test",
                                               "x-notificationstatus": "Test",
                                               "x-subscriptionstatus": "Test",
                                               "x-messageid": "Test"},
                               status=404)

        # Creating MPNS object, posting request and
        # submitting response to parse_response
        test_tile = MPNSTile()
        response = requests.post(test_tile_URI)
        status = test_tile.parse_response(response)

        # Checking status code, error message and ensuring
        # other headers passed without unaltered
        assert status['http_status_code'] == 404
        assert status['error'] == 'Not Found - subscription URI is invalid'
        assert status['drop_subscription'] is True
        assert status['device_connection_status'] == 'Test'
        assert status['subscription_status'] == 'Test'
        assert status['notification_status'] == 'Test'
        assert status['message_id'] == 'Test'

    @httpretty.activate
    def test_parse_response_405(self):
        # Mocking response headers
        test_tile_URI = "http://testuri.com/"
        httpretty.register_uri(httpretty.POST,
                               test_tile_URI,
                               content_type='text/json',
                               adding_headers={"x-deviceconnectionstatus": "Test",
                                               "x-notificationstatus": "Test",
                                               "x-subscriptionstatus": "Test",
                                               "x-messageid": "Test"},
                               status=405)

        # Creating MPNS object, posting request and submitting
        # response to parse_response
        test_tile = MPNSTile()
        response = requests.post(test_tile_URI)
        status = test_tile.parse_response(response)

        # Checking status code, error message and ensuring
        # other headers passed without unaltered
        assert status['http_status_code'] == 405
        assert status['error'] == 'Invalid Method'
        assert status['device_connection_status'] == 'Test'
        assert status['subscription_status'] == 'Test'
        assert status['notification_status'] == 'Test'
        assert status['message_id'] == 'Test'

    @httpretty.activate
    def test_parse_response_406(self):
        # Mocking response headers
        test_tile_URI = "http://testuri.com/"
        httpretty.register_uri(httpretty.POST,
                               test_tile_URI,
                               content_type='text/json',
                               adding_headers={"x-deviceconnectionstatus": "Test",
                                               "x-notificationstatus": "Test",
                                               "x-subscriptionstatus": "Test",
                                               "x-messageid": "Test"},
                               status=406)

        # Creating MPNS object, posting request and
        # submitting response to parse_response
        test_tile = MPNSTile()
        response = requests.post(test_tile_URI)
        status = test_tile.parse_response(response)

        # Checking status code, error message and ensuring
        # other headers passed without unaltered
        assert status['http_status_code'] == 406
        assert status['error'] == 'Not Acceptable - per-day throttling limit reached'
        assert status['backoff_seconds'] == 24*60*60
        assert status['device_connection_status'] == 'Test'
        assert status['subscription_status'] == 'Test'
        assert status['notification_status'] == 'Test'
        assert status['message_id'] == 'Test'

    @httpretty.activate
    def test_parse_response_412(self):
        # Mocking response headers
        test_tile_URI = "http://testuri.com/"
        httpretty.register_uri(httpretty.POST,
                               test_tile_URI,
                               content_type='text/json',
                               adding_headers={"x-deviceconnectionstatus": "Test",
                                               "x-notificationstatus": "Test",
                                               "x-subscriptionstatus": "Test",
                                               "x-messageid": "Test"},
                               status=412)

        # Creating MPNS object, posting request and
        # submitting response to parse_response
        test_tile = MPNSTile()
        response = requests.post(test_tile_URI)
        status = test_tile.parse_response(response)

        # Checking status code, error message and ensuring
        # other headers passed without unaltered
        assert status['http_status_code'] == 412
        assert status['error'] == 'Precondition Failed - device inactive, try once per-hour'
        assert status['backoff_seconds'] == 60*60
        assert status['device_connection_status'] == 'Test'
        assert status['subscription_status'] == 'Test'
        assert status['notification_status'] == 'Test'
        assert status['message_id'] == 'Test'

    @httpretty.activate
    def test_parse_response_503(self):
        # Mocking response headers
        test_tile_URI = "http://testuri.com/"
        httpretty.register_uri(httpretty.POST,
                               test_tile_URI,
                               content_type='text/json',
                               adding_headers={"x-deviceconnectionstatus": "Test",
                                               "x-notificationstatus": "Test",
                                               "x-subscriptionstatus": "Test",
                                               "x-messageid": "Test"},
                               status=503)

        # Creating MPNS object, posting request and
        # submitting response to parse_response
        test_tile = MPNSTile()
        response = requests.post(test_tile_URI)
        status = test_tile.parse_response(response)

        # Checking status code, error message and ensuring
        # other headers passed without unaltered
        assert status['http_status_code'] == 503
        assert status['error'] == 'Service Unavailable - try again later'
        assert status['backoff_seconds'] == 60
        assert status['device_connection_status'] == 'Test'
        assert status['subscription_status'] == 'Test'
        assert status['notification_status'] == 'Test'
        assert status['message_id'] == 'Test'

    @httpretty.activate
    def test_parse_response_505(self):
        # Mocking response headers
        test_tile_URI = "http://testuri.com/"
        httpretty.register_uri(httpretty.POST,
                               test_tile_URI,
                               content_type='text/json',
                               adding_headers={"x-deviceconnectionstatus": "Test",
                                               "x-notificationstatus": "Test",
                                               "x-subscriptionstatus": "Test",
                                               "x-messageid": "Test"},
                               status=505)

        # Creating MPNS object, posting request and
        # submitting response to parse_response
        test_tile = MPNSTile()
        response = requests.post(test_tile_URI)
        status = test_tile.parse_response(response)

        # Checking status code, error message and ensuring
        # other headers passed without unaltered
        assert status['http_status_code'] == 505
        assert status['error'] == 'Unexpected status'
        assert status['device_connection_status'] == 'Test'
        assert status['subscription_status'] == 'Test'
        assert status['notification_status'] == 'Test'
        assert status['message_id'] == 'Test'

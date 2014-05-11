import unittest
import httpretty
import requests

from mpns import MPNSTile


class test_base(unittest.TestCase):
	
	@httpretty.activate
	def test_parse_response_200(self):
		#Mocking response headers
		test_tile_URI = "http://testuri.com/"
		httpretty.register_uri(httpretty.POST, 
								test_tile_URI,
								content_type='text/json',
								adding_headers={
									"x-deviceconnectionstatus":"Test",
									"x-notificationstatus":"Test",
									"x-subscriptionstatus":"Test",
									"x-messageid":"Test"},
								status=200)

		#Creating MPNS object, posting request and submitting response to parse_response
		test_tile = MPNSTile()		
		response = requests.post(test_tile_URI)
		status = test_tile.parse_response(response)

		#Checking status code, error message and ensuring other headers passed without unaltered
		assert status['http_status_code'] == 200
		assert status['device_connection_status'] == 'Test'
		assert status['subscription_status'] == 'Test'
		assert status['notification_status'] == 'Test'
		assert status['message_id'] == 'Test'
		
	@httpretty.activate
	def test_parse_response_200_queue_full(self):
		#Mocking response headers
		test_tile_URI = "http://testuri.com/"
		httpretty.register_uri(httpretty.POST, 
								test_tile_URI,
								content_type='text/json',
								adding_headers={
									"x-deviceconnectionstatus":"Test",
									"x-notificationstatus":"QueueFull",
									"x-subscriptionstatus":"Test",
									"x-messageid":"Test"},
								status=200)

		#Creating MPNS object, posting request and submitting response to parse_response
		test_tile = MPNSTile()		
		response = requests.post(test_tile_URI)
		status = test_tile.parse_response(response)

		#Checking status code, error message and ensuring other headers passed without unaltered
		assert status['http_status_code'] == 200
		assert status['error'] == 'Queue full, try again later'
		assert status['backoff_seconds'] == 60
		assert status['device_connection_status'] == 'Test'
		assert status['subscription_status'] == 'Test'
		assert status['notification_status'] == 'QueueFull'
		assert status['message_id'] == 'Test'
	
	@httpretty.activate
	def test_parse_response_400(self):
		#Mocking response headers
		test_tile_URI = "http://testuri.com/"
		httpretty.register_uri(httpretty.POST, 
								test_tile_URI,
								content_type='text/json',
								adding_headers={
									"x-deviceconnectionstatus":"Test",
									"x-notificationstatus":"Test",
									"x-subscriptionstatus":"Test",
									"x-messageid":"Test"},
								status=400)

		#Creating MPNS object, posting request and submitting response to parse_response
		test_tile = MPNSTile()		
		response = requests.post(test_tile_URI)
		status = test_tile.parse_response(response)

		#Checking status code, error message and ensuring other headers passed without unaltered
		assert status['http_status_code'] == 400
		assert status['error'] == 'Bad Request - invalid payload or subscription URI'
		assert status['device_connection_status'] == 'Test'
		assert status['subscription_status'] == 'Test'
		assert status['notification_status'] == 'Test'
		assert status['message_id'] == 'Test'

		#####Response Logic#####
        # if code == 200:
            # if status['notification_status'] == 'QueueFull':
                # status['error'] = 'Queue full, try again later'
                # status['backoff_seconds'] = 60
        # elif code == 400:
            # status['error'] = 'Bad Request - invalid payload or subscription URI'
        # elif code == 401:
            # status['error'] = 'Unauthorized - invalid token or subscription URI'
            # status['drop_subscription'] = True
        # elif code == 404:
            # status['error'] = 'Not Found - subscription URI is invalid'
            # status['drop_subscription'] = True
        # elif code == 405:
            # status['error'] = 'Invalid Method' # (this should not happen, module uses only POST method)
        # elif code == 406:
            # status['error'] = 'Not Acceptable - per-day throttling limit reached'
            # status['backoff_seconds'] = 24 * 60 * 60
        # elif code == 412:
            # status['error'] = 'Precondition Failed - device inactive, try once per-hour'
            # status['backoff_seconds'] = 60 * 60
        # elif code == 503:
            # status['error'] = 'Service Unavailable - try again later'
            # status['backoff_seconds'] = 60
        # else:
            # status['error'] = 'Unexpected status'

        # return status
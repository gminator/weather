from django.test import TestCase
from openweather.models import OpenWeather,BadDateException, Day
from unittest.mock import patch
from datetime import datetime

# Create your tests here.
class OpenWeatherTests(TestCase):

	def test_test_median_humidity(self,):

		day = Day(hourly=[
			{"temp": 274.15,"humidity": 10, "wind_speed" : 1.60934}, 
			{"temp": 275.15,"humidity": 50, "wind_speed" : 3.21868},
			 {"temp": 276.15, "humidity": 100, "wind_speed": 4.82802}
		]) 
		self.assertEquals(day.median_humidity, 50) 

	def test_test_max_humidity(self,):
		day = Day(hourly=[
			{"temp": 274.15,"humidity": 10, "wind_speed" : 1.60934}, 
			{"temp": 275.15,"humidity": 50, "wind_speed" : 3.21868},
			 {"temp": 276.15, "humidity": 100, "wind_speed": 4.82802}
		])

		self.assertEquals(day.max_humidity, 100) 

	def test_test_min_humidity(self,):
		day = Day(hourly=[
			{"temp": 274.15,"humidity": 10, "wind_speed" : 1.60934}, 
			{"temp": 275.15,"humidity": 50, "wind_speed" : 3.21868},
			 {"temp": 276.15, "humidity": 100, "wind_speed": 4.82802}
		])

		self.assertEquals(day.min_humidity, 10) 


	def test_day_average(self,):
		day = Day(hourly=[
			{"temp": 274.15,"humidity": 10, "wind_speed" : 1.60934}, 
			{"temp": 275.15,"humidity": 50, "wind_speed" : 3.21868},
			 {"temp": 276.15, "humidity": 100, "wind_speed": 4.82802},
			 {"temp": 277.15, "humidity": 100, "wind_speed": 4.82802}
		]) 
		self.assertEquals(day.median_tmp, 2.5) 

	def test_test_median_tmp_no_middle(self,):
		day = Day(hourly=[
			{"temp": 274.15,"humidity": 10, "wind_speed" : 1.60934}, 
			{"temp": 275.15,"humidity": 50, "wind_speed" : 3.21868},
			 {"temp": 276.15, "humidity": 100, "wind_speed": 4.82802},
			 {"temp": 277.15, "humidity": 100, "wind_speed": 4.82802}
		]) 
		self.assertEquals(day.median_tmp, 2.5) 

	def test_test_median_tmp(self,):
		day = Day(hourly=[
			{"temp": 274.15,"humidity": 10, "wind_speed" : 1.60934}, 
			{"temp": 275.15,"humidity": 50, "wind_speed" : 3.21868},
			 {"temp": 276.15, "humidity": 100, "wind_speed": 4.82802}
		]) 
		self.assertEquals(day.median_tmp, 2.0) 

	def test_test_max_tmp(self,):
		day = Day(hourly=[
			{"temp": 274.15,"humidity": 10, "wind_speed" : 1.60934}, 
			{"temp": 275.15,"humidity": 50, "wind_speed" : 3.21868},
			 {"temp": 276.15, "humidity": 100, "wind_speed": 4.82802}
		])

		self.assertEquals(day.max_tmp, 3.0) 

	def test_test_min_tmp(self,):
		day = Day(hourly=[
			{"temp": 274.15,"humidity": 10, "wind_speed" : 1.60934}, 
			{"temp": 275.15,"humidity": 50, "wind_speed" : 3.21868},
			 {"temp": 276.15, "humidity": 100, "wind_speed": 4.82802}
		])

		self.assertEquals(day.min_tmp, 1.0) 

	def test_celius_constructor(self,):
		day = Day(hourly=[
			{"temp": 274.15,"humidity": 10, "wind_speed" : 1.60934}, 
			{"temp": 275.15,"humidity": 50, "wind_speed" : 3.21868},
			 {"temp": 276.15, "humidity": 100, "wind_speed": 4.82802}
		])
		self.assertEquals(day.tmps, [1.0,2.0,3.0]) 
		self.assertEquals(day.humids, [10,50,100]) 
		self.assertEquals(day.winds, [1,2,3]) 

	def test_past_days_invalid_date(self,):
		weather = OpenWeather() 
		with self.assertRaises(BadDateException) as context:
			weather.weather_on(units="c",lat=0, lon=0,dt=123453)	

	def test_past_days(self,):
		now = datetime.now()
		weather = OpenWeather()  
		
		def api_response(*args, **kwargs):
			return FakeResponse({"hourly" : [{"temp": 274.15,"humidity": 10, "wind_speed" : 1.60934}]})

		with patch('requests.request', api_response): 
			day = weather.weather_on(units="c",lat=0, lon=0,dt=now.timestamp(), stub=now)
			self.assertIsInstance(day, Day)

		
class FakeResponse(object):
	def __init__(self,json):
		self.data = json

	def json(self,):
		return self.data
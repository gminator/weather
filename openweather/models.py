from django.db import models
import requests
from  datetime import datetime, timedelta
import math

class Day(object): 

	def unit(self,temp):
		return round({
			"c" : temp-273.15,
			"k" : temp,
			"f" : (((temp-274.15)/5) * 9) + 32,
		}[self.units], 2)

	def __init__(self, **kwargs):
		self.lat = kwargs["lat"] if "lat" in kwargs else None
		self.lng = kwargs["lon"] if "lon" in kwargs else None
		self.tz = kwargs["timezone"] if "timezone" in kwargs else None
		self.hourly = kwargs["hourly"] if "hourly" in kwargs else []
		self.units = kwargs["units"] if "units" in kwargs else "c"


		self.tmps = [self.unit(hour["temp"]) if "temp" in hour else None for hour in kwargs["hourly"]]
		self.humids = [hour["humidity"] if "humidity" in hour else None for hour in kwargs["hourly"]]
		self.winds = [round(hour["wind_speed"] /1.60934,2) if "wind_speed" in hour else None for hour in kwargs["hourly"]]

	
	@property
	def median_humidity(self,):
		return self.median(self.humids)

	@property
	def min_humidity(self,):
		return self.min(self.humids)

	@property
	def max_humidity(self,):
		return self.max(self.humids)


	@property
	def avg_humidity(self,):
		return self.average(self.humids)

	@property
	def avg_tmp(self,):
		return self.average(self.tmps)

	@property
	def median_tmp(self,):
		return self.median(self.tmps)

	@property
	def min_tmp(self,):
		return self.min(self.tmps)

	@property
	def max_tmp(self,):
		return self.max(self.tmps)

	def min(self,data):
		return min(data)

	def max(self,data):
		return max(data)

	def median(self,data):
		data.sort()
		l = len(data) 
		#Event Numbers
		if l % 2  == 0:
			f = int((l/2) - 1)
			return round((data[f] + data[f + 1])/2,2)

		i = l//2
		return data[i]

	def average(sefl,data):
		return round(sum(data)/len(data),2)

	def serialize(self,):
		return {
			"temp" : {
				"min" : self.min_tmp,
				"max" : self.max_tmp,
				"median" : self.median_tmp,
				"avg" : self.avg_tmp,
			},
			"humidity" : {
				"min" : self.min_humidity,
				"max" : self.max_humidity,
				"median" : self.median_humidity,
				"avg" : self.avg_humidity,
			},
			"graph" : self.graph()
		}

	def graph(self,):
		data = {}
		for row in self.hourly:
			key = datetime.fromtimestamp(row["dt"]).strftime("%Y-%m-%d %H:%M")
			if key not in data:
				data[key] = [self.unit(row["temp"]), row["humidity"]]
		graph = [["Date", "Temp", "Humidity"]]

		for date,values in data.items():
			graph.append([date] + values) 
		return graph



# Create your models here.
class OpenWeather(object):
	def __init__(self,):
		self.uri = "https://community-open-weather-map.p.rapidapi.com/"
		self.key = "06eafc15dbmsh348f712812a3bf8p136ec0jsn8b48402aa070"

	def headers(self,):
		return {
			#"x-rapidapi-host": "community-open-weather-map.p.rapidapi.com",
			"x-rapidapi-key": self.key,
			#"useQueryString": 'true'
		}

	def weather_on(self,**kwargs):   
		"""
		Past Data
		Get pass Weather Data 
		Up to 5 Days

		@param dt int Unix Time Stamp 
		"""
		current_date = datetime.now()

		if "stub" in kwargs:
			current_date = kwargs["stub"] 

		limit = current_date - timedelta(days=5) 
		if kwargs["dt"] < limit.timestamp():
			raise BadDateException("Your date exceeds the the 5 day limit")
			
		if "dt" not in kwargs or kwargs["dt"] == None: raise BadRequest("Please set a time")
		if "lat" not in kwargs or kwargs["lat"] == None: raise BadRequest("Please set a lattitude")
		if "lon" not in kwargs or kwargs["lon"] == None: raise BadRequest("Please set a longtitude")

		

		#raise Exception(kwargs)
		response = requests.request("GET", self.uri + "onecall/timemachine", 
									headers=self.headers(), 
									params=kwargs)

		return Day(units=kwargs["units"], **response.json())




class BadDateException(Exception): pass
class BadRequest(Exception): pass
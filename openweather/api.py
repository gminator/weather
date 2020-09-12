from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication 
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from openweather.models import OpenWeather, BadRequest
from datetime import datetime
from rest_framework import status

class WeatherViewSet(viewsets.ViewSet): 
    def list(self, request):
    	
    	weather = OpenWeather()
    	try: 
    		day = weather.weather_on(
				dt=int(datetime.strptime(request.GET["date"], "%Y/%m/%d").timestamp()) if "date" in request.GET else None, 
				lat=request.GET["lat"] if "lat" in request.GET else None,
	    		lon=request.GET["lng"] if "lng" in request.GET else None,
	    		units=request.GET["unit"] if "unit" in request.GET else "c"
			)
    	except BadRequest as e:
    		return Response({"error" : str(e)}, status=status.HTTP_400_BAD_REQUEST)
    	except Exception as e:
    		raise e
    		return Response({"error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    	return Response(day.serialize())
    	
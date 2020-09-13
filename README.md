# Weather App
A basic weather app that returns Min, Max, Median, and Average for a Given Day (Up to 5 Days In The Past). 

It backs off the OpenWeatherMaps API and makes use of Python3 with Django & Django-rest-framework. 

I did not make use of any of the Auth Backends on the FrontEnd or API for ease of use.

# Front End 

It makes use of Vali Admin for the Front-end Libs, this package gives out of the box bootstrap and mobile responsiveness support. The application is hosted on an EC2 instance running Gunicorn and Nginx. It has Cloudflare in front of it for caching, SSL, and additional security. 

The front end can be found at: 

```
https://weather.statnav.co.za/weather/
```

# Rest API 

The API Can be found here, I did not make use of the serializers and ModelViewSets since I’m not writing anything into a DB.

Tha API Accepts a date (up to 5 days in the past), a Lat, Lng, and a unit of measurement for the Temperature. 

K (Kelvin)
C (Celsius)
F (Fahrenheit)

```
curl -X GET \
  'https://weather.statnav.co.za/api/weather/?unit=k&date=2020%2F09%2F12&lat=-33.8767921&lng=18.5311788'
 ```
 
This API is also consumed by the FrontEnd, it will return the ranges as well data suitable for plotting on Google Charts. 

# Unit Tests

The application supports unit tests for basic scenarios for the calculation of Min, Max, Median & Average. 
It also tests the API Integration through the use of python Mock Framework 


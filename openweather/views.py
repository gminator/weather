from django.shortcuts import render
from django.views.generic import TemplateView, ListView,ListView, DetailView,View 

class OpenWeatherView(TemplateView):
	template_name = "weather.html"


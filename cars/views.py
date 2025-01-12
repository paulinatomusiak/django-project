from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from cars.models import Car

# Create your views here.

class CarsListView(ListView):
    model = Car
    template_name = "cars_list.html"

class CarDetailView(DetailView):
    model = Car
    template_name = "car_detail.html"
from django.urls import include, path

from cars.views import CarsListView, CarDetailView


urlpatterns = [
    path('', CarsListView.as_view(), name="cars-list"),
    path("<int:pk>/", CarDetailView.as_view(), name="car-detail"),
]
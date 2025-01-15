from django.urls import include, path

from cars.views import (
    CarsListView,
    CarDetailView,
    create_reservation,
    delete_reservation,
    ReservationDetailView,
)


urlpatterns = [
    path("", CarsListView.as_view(), name="cars-list"),
    path("<int:pk>/", CarDetailView.as_view(), name="car-detail"),
    path("<int:pk>/reserve", create_reservation, name="car-reserve"),
    path("reservation/<int:pk>/delete/", delete_reservation, name="delete-reservation"),
    path(
        "reservation/<int:pk>/",
        ReservationDetailView.as_view(),
        name="reservation-detail",
    ),
]

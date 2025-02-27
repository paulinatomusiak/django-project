from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.views.decorators.csrf import csrf_protect
from django.http import HttpRequest, HttpResponse
from cars.models import Car, Reservation
from cars.filters import CarFilter
from cars.forms import ReservationForm
from django_filters.views import FilterView
from typing import Any
from django.contrib.auth.decorators import login_required


class CarsListView(FilterView):
    model = Car
    template_name = "cars_list.html"
    filterset_class = CarFilter
    context_object_name = "object_list"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["record_count"] = context["object_list"].count()
        return context


class CarDetailView(DetailView):
    model = Car
    template_name = "car_detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = ReservationForm()
        return context


@csrf_protect
def create_reservation(request: HttpRequest, pk: int) -> HttpResponse:
    car = get_object_or_404(Car, pk=pk)
    if request.method == "POST" and request.user.is_authenticated:
        form = ReservationForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]

            overlapping_reservations = Reservation.objects.filter(
                car=car,
                start_date__lte=end_date,
                end_date__gte=start_date,
            )
            if overlapping_reservations.exists():
                form.add_error(
                    None, "Samochód jest już zarezerwowany w wybranym terminie."
                )
            else:
                Reservation.objects.create(
                    car=car,
                    user=request.user,
                    start_date=start_date,
                    end_date=end_date,
                )
                return redirect("user-detail", request.user.id)

        return render(request, "car_detail.html", {"car": car, "form": form})

    return redirect("cars-list")


@login_required
def delete_reservation(request: HttpRequest, pk: int) -> HttpResponse:
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    reservation.delete()
    return redirect("user-detail", request.user.id)


class ReservationDetailView(DetailView):
    model = Reservation
    template_name = "reservation_detail.html"
    context_object_name = "reservation"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reservation = self.get_object()

        days = (reservation.end_date - reservation.start_date).days + 1
        total_price = days * reservation.car.daily_rate

        context["total_price"] = total_price
        return context

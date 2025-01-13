from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.views.decorators.csrf import csrf_protect
from django.http import HttpRequest, HttpResponse
from cars.models import Car, Reservation
from cars.filters import CarFilter
from cars.forms import ReservationForm
from django_filters.views import FilterView
from typing import Any


class CarsListView(FilterView):
    model = Car
    template_name = "cars_list.html"
    filterset_class = CarFilter
    context_object_name = "object_list"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["record_count"] = context[
            "object_list"
        ].count()  # Liczba wyników filtrowania
        return context


class CarDetailView(DetailView):
    model = Car
    template_name = "car_detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = ReservationForm()
        return context


@csrf_protect
def create_reservation(request: HttpRequest, pk: int) -> HttpResponse | None:
    if request.method == "POST" and request.user.is_authenticated:
        form = ReservationForm(request.POST)
        car = get_object_or_404(Car, pk=pk)
        if form.is_valid():
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]
            if start_date > end_date:
                start_date, end_date = end_date, start_date
            if not car.is_selected_days_reserved(start_date, end_date):
                Reservation.objects.create(
                    car=car,
                    user=request.user,
                    start_date=start_date,
                    end_date=end_date,
                )
                return redirect("cars-list")
                # TODO:przekierowanie profil
        else:
            return render(request, "car_detail.html", {"object": car, "form": form})
    return redirect("cars-list")

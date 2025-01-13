from datetime import date
from django import forms
import django_filters
from cars.models import Car
from django.db.models import QuerySet


class CarFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name="start_date",
        label="Początek rezerwacji",
        widget=forms.DateInput(attrs={"type": "date"}),
        method="filter_date_range",
    )
    end_date = django_filters.DateFilter(
        field_name="end_date",
        label="Koniec rezerwacji",
        widget=forms.DateInput(attrs={"type": "date"}),
        method="filter_date_range",
    )

    brand = django_filters.ChoiceFilter(
        field_name="brand",
        label="Marka",
        choices=lambda: [
            (brand, brand)
            for brand in Car.objects.values_list("brand", flat=True).distinct()
        ],
    )

    seats = django_filters.ChoiceFilter(
        field_name="seats",
        label="Liczba miejsc",
        choices=Car.SEATS_CHOICES,
    )

    car_type = django_filters.ChoiceFilter(
        field_name="car_type",
        label="Typ samochodu",
        choices=Car.CAR_TYPE_CHOICES,
    )

    fuel_type = django_filters.ChoiceFilter(
        field_name="fuel_type",
        label="Rodzaj paliwa",
        choices=Car.FUEL_TYPE_CHOICES,
    )

    transmission = django_filters.ChoiceFilter(
        field_name="transmission",
        label="Skrzynia biegów",
        choices=Car.TRANSMISSION_CHOICES,
    )

    class Meta:
        model = Car
        fields = ["brand", "seats", "car_type", "fuel_type", "transmission"]

    def filter_date_range(
        self, queryset: QuerySet[Car], name: str, value: date | None
    ) -> QuerySet[Car]:
        start_date = self.data.get("start_date")
        end_date = self.data.get("end_date")

        if start_date and end_date:
            car_filter = ~Car.get_selected_days_reserved_filter(start_date, end_date)
            queryset = queryset.filter(car_filter)

        return queryset

from django.db import models
from management.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import os
import random
from django.db.models import Q


class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ("manual", "Manualna"),
        ("automatic", "Automatyczna"),
    ]

    FUEL_TYPE_CHOICES = [
        ("petrol", "Benzyna"),
        ("diesel", "Diesel"),
        ("electric", "Elektryczny"),
        ("hybrid", "Hybrydowy"),
    ]

    CAR_TYPE_CHOICES = [
        ("sedan", "Sedan"),
        ("hatchback", "Hatchback"),
        ("suv", "SUV"),
        ("coupe", "Coupe"),
        ("convertible", "Kabriolet"),
        ("wagon", "Kombi"),
    ]

    DOORS_CHOICES = [(2, 2), (3, 3), (4, 4), (5, 5)]
    SEATS_CHOICES = [(2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)]

    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(1999), MaxValueValidator(2025)]
    )
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    doors = models.PositiveIntegerField(choices=DOORS_CHOICES)
    car_type = models.CharField(max_length=20, choices=CAR_TYPE_CHOICES)
    transmission = models.CharField(max_length=10, choices=TRANSMISSION_CHOICES)
    seats = models.PositiveIntegerField(choices=SEATS_CHOICES)
    fuel_type = models.CharField(max_length=10, choices=FUEL_TYPE_CHOICES)
    trunk_size = models.PositiveIntegerField(help_text="Pojemność bagażnika w litrach")
    image = models.CharField(max_length=255, blank=True, null=True)

    @property
    def name(self) -> str:
        return f"{self.brand} {self.model}"

    @property
    def is_reserved(self):
        return self.reservations.all().exists()

    def __str__(self) -> str:
        return f"{self.brand} {self.model} ({self.year}) Samochód {self.name} id: {self.id}"

    @staticmethod
    def assign_random_photo() -> str | None:
        photos_dir = os.path.join("cars", "static", "car_photos")
        valid_extensions = {".jpeg", ".jpg", ".png"}

        photos = [
            file
            for file in os.listdir(photos_dir)
            if os.path.isfile(os.path.join(photos_dir, file))
            and os.path.splitext(file)[1].lower() in valid_extensions
        ]

        if photos:
            return f"car_photos/{random.choice(photos)}"
        return None

    def save(self, *args: tuple, **kwargs: dict) -> None:
        if not self.image:
            self.image = self.assign_random_photo()
        super().save(*args, **kwargs)

    def is_selected_days_reserved(self, new_start_date, new_end_date):
        check = Car.get_selected_days_reserved_filter(new_start_date, new_end_date)
        return Car.objects.filter(check, id=self.id).exists()

    @staticmethod
    def get_selected_days_reserved_filter(new_start_date, new_end_date):
        return Q(
            reservations__start_date__lt=new_end_date,
            reservations__end_date__gt=new_start_date,
        )


class Reservation(models.Model):
    car = models.ForeignKey(Car, on_delete=models.PROTECT, related_name="reservations")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(verbose_name="Start of reservation")
    end_date = models.DateField(verbose_name="End of reservation")

    def __str__(self) -> str:
        return f"Reservation {self.id} car {self.car}"

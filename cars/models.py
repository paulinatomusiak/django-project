from django.db import models
from management.models import User
from django.core.validators import MaxValueValidator, MinValueValidator



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
    year = models.PositiveIntegerField(validators=[MinValueValidator(1999), MaxValueValidator(2025)]
)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    doors = models.PositiveIntegerField(choices=DOORS_CHOICES)
    car_type = models.CharField(max_length=20, choices=CAR_TYPE_CHOICES)
    transmission = models.CharField(max_length=10, choices=TRANSMISSION_CHOICES)
    seats = models.PositiveIntegerField(choices=SEATS_CHOICES)
    fuel_type = models.CharField(max_length=10, choices=FUEL_TYPE_CHOICES)
    trunk_size = models.PositiveIntegerField(help_text="Pojemność bagażnika w litrach")
    is_available = models.BooleanField(default=True)

    @property
    def name(self):
        return f"{self.brand} {self.model}"

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year}) Samochód {self.name} id: {self.id}"


class Reservation(models.Model):
    car = models.ForeignKey(Car, on_delete=models.PROTECT, related_name="reservations")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(verbose_name="Start of reservation")
    end_date = models.DateField(verbose_name="End of reservation")

    def __str__(self):
        return f"Reservation {self.id} car {self.car}"

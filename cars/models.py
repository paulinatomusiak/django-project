from django.db import models
from management.models import User

class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
    ]

    FUEL_TYPE_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ]

    CAR_TYPE_CHOICES = [
        ('sedan', 'Sedan'),
        ('hatchback', 'Hatchback'),
        ('suv', 'SUV'),
        ('coupe', 'Coupe'),
        ('van', 'Van'),
    ]

    DOORS_CHOICES = [
        (2, '2 doors'),
        (3, '3 doors'),
        (4, '4 doors'),
        (5, '5 doors'),
    ]

    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    doors = models.PositiveIntegerField(choices=DOORS_CHOICES)
    car_type = models.CharField(max_length=20, choices=CAR_TYPE_CHOICES)
    transmission = models.CharField(max_length=10, choices=TRANSMISSION_CHOICES)
    seats = models.PositiveIntegerField()
    fuel_type = models.CharField(max_length=10, choices=FUEL_TYPE_CHOICES)
    trunk_size = models.PositiveIntegerField(help_text="Trunk capacity in liters")
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
    end_date = models.DateField(verbose_name="End of reservationi")

    def __str__(self):
        return f"Reservation {self.id} car {self.car}"

import random
from typing import Any
from django.core.management.base import BaseCommand
from datetime import date, timedelta, datetime
from cars.models import Car, Reservation
from management.models import User


def random_date(start: date, end: date) -> date:
    """
    This function will return a random date between two date objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randint(0, int_delta)
    random_date = start + timedelta(seconds=random_second)
    return date(random_date.year, random_date.month, random_date.day)


def to_date(passed_date: date) -> date:
    return date(passed_date.year + 10, passed_date.month, passed_date.day)


class Command(BaseCommand):
    help = "Creates car reservations for development"

    def handle(self, *args: Any, **options: Any) -> None:
        user: User | None = User.objects.first()
        if not user:
            self.stdout.write(
                self.style.ERROR("No users found. Please create a user first.")
            )
            return

        cars = Car.objects.filter(id__range=(10, 20))
        if not cars.exists():
            self.stdout.write(self.style.ERROR("No cars found with IDs from 10 to 20."))
            return

        for _ in range(10):
            car: Car = random.choice(cars)
            start_date: date = random_date(date(2025, 1, 1), datetime.now().date())
            end_date: date = random_date(
                start_date, datetime.now().date() + timedelta(days=30)
            )

            if not car.is_selected_days_reserved(start_date, end_date):
                Reservation.objects.create(
                    user=user,
                    car=car,
                    start_date=start_date,
                    end_date=end_date,
                )

                self.stdout.write(
                    f"Reservation created for Car {car.id} from {start_date} to {end_date}."
                )

        self.stdout.write(self.style.SUCCESS("10 car reservations have been created."))

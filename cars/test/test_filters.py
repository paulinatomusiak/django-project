from datetime import date
import random
from assertpy import assert_that
from django.test import TestCase
from cars.filters import CarFilter
from cars.models import Car, Reservation
from management.models import User


class TestCarFiltersAndReservations(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user: User = User.objects.create_user(
            username="test_user", password="12345"
        )

        cls.car1 = Car.objects.create(
            brand="Toyota",
            seats=5,
            car_type="suv",
            fuel_type="diesel",
            transmission="manual",
            year=2020,
            daily_rate=random.randint(100, 500),
            doors=random.randint(2, 5),
            trunk_size=random.randint(200, 600),
        )

        cls.car2: Car = Car.objects.create(
            brand="Honda",
            seats=4,
            car_type="sedan",
            fuel_type="petrol",
            transmission="automatic",
            year=2022,
            daily_rate=random.randint(100, 500),
            doors=random.randint(2, 5),
            trunk_size=random.randint(200, 600),
        )

        cls.reservation1: Reservation = Reservation.objects.create(
            car=cls.car1,
            user=cls.user,
            start_date=date(2025, 4, 10),
            end_date=date(2025, 4, 15),
        )
        cls.reservation2: Reservation = Reservation.objects.create(
            car=cls.car2,
            user=cls.user,
            start_date=date(2025, 4, 20),
            end_date=date(2025, 4, 25),
        )

    def test_car_reserved(self) -> None:
        start_date: date = date(2025, 4, 13)
        end_date: date = date(2025, 4, 15)

        is_reserved: bool = self.car1.is_selected_days_reserved(start_date, end_date)
        assert_that(is_reserved).is_true()

    def test_filter_exclude_reserved_car(self) -> None:
        start_date: date = date(2025, 4, 12)
        end_date: date = date(2025, 4, 14)
        car_filter: CarFilter = CarFilter(
            data={"start_date": start_date, "end_date": end_date}
        )
        filtered_cars = car_filter.qs
        assert_that(filtered_cars).does_not_contain(self.car1)
        assert_that(filtered_cars).contains(self.car2)

    def test_filter_by_brand(self) -> None:
        car_filter: CarFilter = CarFilter(data={"brand": "Toyota"})
        filtered_cars = car_filter.qs

        assert_that(filtered_cars).contains(self.car1).does_not_contain(self.car2)

    def test_filter_by_seats(self) -> None:
        car_filter: CarFilter = CarFilter(data={"seats": 5})
        filtered_cars = car_filter.qs
        assert_that(filtered_cars).contains(self.car1).does_not_contain(self.car2)

    def test_filter_by_fuel(self) -> None:
        car_filter: CarFilter = CarFilter(data={"fuel_type": "petrol"})
        filtered_cars = car_filter.qs
        assert_that(filtered_cars).contains(self.car2).does_not_contain(self.car1)

    def test_filter_by_car_type(self) -> None:
        car_filter = CarFilter(data={"car_type": "suv"})
        filtered_cars = car_filter.qs
        assert_that(filtered_cars).contains(self.car1).does_not_contain(self.car2)

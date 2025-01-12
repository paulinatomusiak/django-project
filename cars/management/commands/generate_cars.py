import random
from django.core.management.base import BaseCommand
from cars.models import Car


class Command(BaseCommand):
    help = "Generates sample car data for development"
    number_of_generated_cars = 15

    def handle(self, number_of_generated_cars: int, *args, **options) -> None:
        TRANSMISSION_CHOICES: list[str] = ["manual", "automatic"]
        FUEL_TYPE_CHOICES: list[str] = ["petrol", "diesel", "electric", "hybrid"]

        car_types: dict = {
            "sedan": {"photo": "car_photos/1.jpeg", "seats": 5, "doors": 4},
            "hatchback": {"photo": "car_photos/5.jpeg", "seats": 5, "doors": 5},
            "suv": {
                "photo": "car_photos/6.jpeg",
                "seats": random.choice([5, 7]),
                "doors": 5,
            },
            "coupe": {"photo": "car_photos/3.jpeg", "seats": 2, "doors": 2},
            "wagon": {
                "photo": "car_photos/4.jpeg",
                "seats": random.randint(5, 9),
                "doors": 5,
            },
            "convertible": {"photo": "car_photos/2.jpeg", "seats": 2, "doors": 2},
        }

        for _ in range(number_of_generated_cars):
            car_type: str = random.choice(list(car_types.keys()))
            car_data: dict[str, int | str] = car_types[car_type]

            car: Car = Car.objects.create(
                brand=random.choice(
                    ["Toyota", "Ford", "BMW", "Audi", "Mercedes", "Tesla"]
                ),
                model=f"Model-{random.randint(1, 1000)}",
                year=random.randint(2000, 2025),
                daily_rate=round(random.uniform(50, 500), 2),
                doors=car_data["doors"],
                car_type=car_type,
                transmission=random.choice(TRANSMISSION_CHOICES),
                seats=car_data["seats"],
                fuel_type=random.choice(FUEL_TYPE_CHOICES),
                trunk_size=random.randint(200, 600),
                image=car_data["photo"],
            )

            self.stdout.write(
                f"Added car: {car.brand} {car.model}, Type: {car_type}, Photo: {car_data['photo']}"
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully generated {number_of_generated_cars} cars"
            )
        )

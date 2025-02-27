from django.contrib import admin
from cars.models import Car, Reservation


# Register your models here.


class CarAdmin(admin.ModelAdmin):
    list_display = ["id", "brand", "model", "year"]
    fields = [
        "brand",
        "model",
        "year",
        "daily_rate",
        "doors",
        "car_type",
        "transmission",
        "seats",
        "fuel_type",
        "trunk_size",
        "image",
    ]
    readonly_fields = ["is_reserved"]


admin.site.register(Car, CarAdmin)
admin.site.register(Reservation)

from django.forms import ModelForm, ValidationError, widgets
from django.utils.timezone import now
from datetime import date
from cars.models import Reservation


class ReservationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.car = kwargs.pop("car", None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Reservation
        fields = ["start_date", "end_date"]
        widgets = {
            "start_date": widgets.DateInput(attrs={"type": "date"}),
            "end_date": widgets.DateInput(attrs={"type": "date"}),
        }

    def clean_start_date(self) -> date:
        start_date: date = self.cleaned_data["start_date"]
        date_now = now()
        today: date = date(date_now.year, date_now.month, date_now.day)
        if start_date < today:
            raise ValidationError("Data początkowa rezerwacji nie może być z przeszłości.")
        return start_date

    def clean_end_date(self) -> date:
        end_date: date = self.cleaned_data["end_date"]
        date_now = now()
        today: date = date(date_now.year, date_now.month, date_now.day)
        if end_date < today:
            raise ValidationError("Data końcowa rezerwacji nie może być z przeszłości.")
        return end_date

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and self.car:
            overlapping_reservations = Reservation.objects.filter(
                car=self.car,
                start_date__lte=end_date,
                end_date__gte=start_date,
            )
            if overlapping_reservations.exists():
                raise ValidationError("Samochód jest już zarezerwowany w wybranym terminie.")
        return cleaned_data

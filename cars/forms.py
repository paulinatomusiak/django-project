from django.forms import ModelForm, ValidationError, widgets
from django.utils.timezone import now
from datetime import date
from cars.models import Reservation


class ReservationForm(ModelForm):
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
            raise ValidationError("Start_date cannot be from the past")
        return start_date

    def clean_end_date(self) -> date:
        end_date: date = self.cleaned_data["end_date"]
        date_now = now()
        today: date = date(date_now.year, date_now.month, date_now.day)
        if end_date < today:
            raise ValidationError("End_date cannot be from the past")
        return end_date

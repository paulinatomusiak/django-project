from typing import Any
from django.views.generic.detail import DetailView

from cars.models import Reservation
from management.models import User
from django.utils.timezone import now


class UserDetailView(DetailView):
    model = User
    template_name = "user_detail.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["reservations"] = Reservation.objects.filter(
            user_id=self.object.id, start_date__gte=now()
        )
        return context

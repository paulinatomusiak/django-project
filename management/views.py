from typing import Any
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth import login, authenticate
from django.http import HttpRequest, HttpResponse
from cars.models import Reservation
from management.models import User
from management.forms import CustomUserCreationForm
from django.utils.timezone import now
from django.contrib import messages


def login_register_view(request):
    login_form = AuthenticationForm()
    register_form = CustomUserCreationForm()

    if request.method == "POST":
        if "login" in request.POST:
            login_form = AuthenticationForm(data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect("cars-list")
            else:
                messages.error(request, "Wprowadzono błędne dane.")

        elif "register" in request.POST:
            register_form = CustomUserCreationForm(data=request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                messages.success(request, "Konto stworzono pomyślnie")
                return redirect("cars-list")
            else:
                messages.error(request, "Wystąpił problem w trakcie rejestracji.")

    return render(
        request,
        "login_register.html",
        {
            "login_form": login_form,
            "register_form": register_form,
        },
    )


class CustomLogoutView(LogoutView):
    def dispatch(
        self, request: HttpRequest, *args: tuple, **kwargs: dict
    ) -> HttpResponse:
        self.handle_logout_message(request)
        return super().dispatch(request, *args, **kwargs)

    def handle_logout_message(self, request: HttpRequest) -> None:
        storage = messages.get_messages(request)
        storage.used = True
        messages.success(request, "Wylogowano pomyślnie!")


class UserDetailView(DetailView):
    model = User
    template_name = "user_detail.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["reservations"] = Reservation.objects.filter(
            user_id=self.object.id, start_date__gte=now()
        )
        return context

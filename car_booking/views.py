from django.shortcuts import redirect


def home_view(request):
    if request.user.is_authenticated:
        return redirect("cars-list")
    return redirect("login-register")

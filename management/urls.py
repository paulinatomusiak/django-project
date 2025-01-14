from django.urls import path
from django.contrib.auth.views import LogoutView
from management.views import login_register_view, UserDetailView, CustomLogoutView

urlpatterns = [
    path("user/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path('auth/login-register/', login_register_view, name='login-register'),
    path('auth/logout/', CustomLogoutView.as_view(next_page='login-register'), name='logout'),
]

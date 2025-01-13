from django.urls import path
from management.views import UserDetailView

urlpatterns = [
    path("user/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
]

from django.urls import include, path

from .views import UserListCreateView, UserDetailView

urlpatterns = [
    path("all-profiles", UserListCreateView.as_view(), name="all-profiles"),
    path("profile/<int:pk>", UserDetailView.as_view(), name="profile")
]
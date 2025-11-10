from django.urls import path
from people import views

urlpatterns = [
    path("", views.list_people, name="list_people"),
    path("profile_details/<int:user_id>/", views.profile_details, name="profile_details"),
    path("get_verified/<int:pk>/", views.get_verified, name="get_verified")
]
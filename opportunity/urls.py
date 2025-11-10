from django.urls import path
from opportunity import views

urlpatterns = [
    path("", views.list_opportunities, name="list_opportunities"),
    path("opportunity_details/<int:opportunity_id>", views.opportunity_details, name="opportunity_details"),
    path("apply/<int:pk>", views.apply, name="apply"),
    path("post_opportunity/", views.post_opportunity, name="post_opportunity"),
    path("edit_opportunity/<int:opportunity_id>", views.edit_opportunity, name="edit_opportunity"),
    path("delete_opportunity/<int:opportunity_id>", views.delete_opportunity, name="delete_opportunity"),
    path("report_opportunity/<int:opportunity_id>", views.report_opportunity, name="report_opportunity"),
]
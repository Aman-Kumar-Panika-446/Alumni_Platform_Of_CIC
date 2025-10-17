from django.urls import path
from events import views
urlpatterns = [
    path("list_events/", views.list_events, name="list_events"),
    path("event_detail/<int:event_id>", views.event_detail, name="event_detail"),
    path("post_event/", views.post_event, name="post_event"),
    path("edit_event/<int:event_id>", views.edit_event, name="edit_event"),
    path("delete_event/<int:event_id>", views.delete_event, name="delete_event"),
    path("report_event/<int:event_id>", views.report_event, name="report_event"),
]
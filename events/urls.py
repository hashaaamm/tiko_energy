from django.urls import path
from .views import EventsListCreateView

urlpatterns = [
    path("", EventsListCreateView.as_view(), name="events-list-create"),
]

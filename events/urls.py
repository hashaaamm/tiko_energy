from django.urls import path
from .views import EventsListCreateView, EventsDetailUpdateView

urlpatterns = [
    path("", EventsListCreateView.as_view(), name="events-list-create"),
    path("<int:pk>/", EventsDetailUpdateView.as_view(), name="events-detail-update"),
]

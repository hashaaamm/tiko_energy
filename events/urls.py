from django.urls import path
from .views import EventsListCreateView, EventsDetailView

urlpatterns = [
    path("", EventsListCreateView.as_view(), name="events-list-create"),
    path("<int:pk>/", EventsDetailView.as_view(), name="events-detail"),
]

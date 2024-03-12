from django.urls import path

from .views import (EventsDetailUpdateView, EventsListCreateView,
                    EventSubscribeAndUnsubscribeView)

urlpatterns = [
    path("", EventsListCreateView.as_view(), name="events-list-create"),
    path("<int:pk>/", EventsDetailUpdateView.as_view(), name="events-detail-update"),
    path(
        "<int:pk>/subscribe/",
        EventSubscribeAndUnsubscribeView.as_view(),
        name="events-subscribe",
    ),
    path(
        "<int:pk>/unsubscribe/",
        EventSubscribeAndUnsubscribeView.as_view(),
        name="events-unsubscribe",
    ),
]

from rest_framework import generics
from .models import Event
from .serializers import (
    EventListCreateSerializer,
    EventDetailUpdateSerializer,
)
from rest_framework import permissions

from .mixins import QuerysetFilterMixin


class EventsListCreateView(QuerysetFilterMixin, generics.ListCreateAPIView):
    """
    This view allows list without login and create with login and allow search using basic params such as:
    status: past,future,cancelled
    id,name,owner,description,event_type
    """

    queryset = Event.objects.all()
    serializer_class = EventListCreateSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filter_queryset(queryset)


class EventsDetailUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Event.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = EventDetailUpdateSerializer

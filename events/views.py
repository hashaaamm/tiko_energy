from rest_framework import generics
from django.db.models import Q
from .models import Event
from .serializers import (
    EventListCreateSerializer,
)
from rest_framework import permissions
from rest_framework import status
from django.utils import timezone
from rest_framework.response import Response
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

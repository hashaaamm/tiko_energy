from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .mixins import QuerysetFilterMixin
from .models import Event
from .permissions import IsOwnerOrReadOnly
from .serializers import (EventDetailUpdateSerializer,
                          EventListCreateSerializer, EventSubscribeSerializer)


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
    """This view allow user to only Retrieve and update the specific event"""

    queryset = Event.objects.all()
    serializer_class = EventDetailUpdateSerializer
    permission_classes = [IsOwnerOrReadOnly]


class EventSubscribeAndUnsubscribeView(generics.UpdateAPIView):
    """This view is for subscribing and unsubscribing to the event. This update list_of_attendees"""

    queryset = Event.objects.all()
    serializer_class = EventSubscribeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        event = self.get_object()
        serializer = self.get_serializer(event, data={})
        serializer.is_valid()
        data = serializer.save()
        status_code = (
            status.HTTP_200_OK if data["success"] else status.HTTP_400_BAD_REQUEST
        )

        return Response({"message": data["message"]}, status=status_code)

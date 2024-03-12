from rest_framework import generics
from django.db.models import Q
from .models import Event
from .serializer import (
    EventCreateSerializer,
    EventListSerializer,
)
from rest_framework import permissions
from rest_framework import status
from django.utils import timezone
from rest_framework.response import Response


class EventsListCreateView(generics.ListCreateAPIView):
    """
    This view allows list without login and create with login and allow search using basic params such as:
    status: past,future,cancelled
    id,name,owner,description,event_type
    """

    queryset = Event.objects.all()

    def get_permissions(self):
        if self.request.method == "POST":
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return EventCreateSerializer
        return EventListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search_params = self.request.query_params.dict()
        if search_params:
            query = Q()
            try:
                for key, value in search_params.items():
                    if key == "status":
                        if value == "past":
                            queryset = queryset.filter(end_date__lt=timezone.now())
                        elif value == "future":
                            queryset = queryset.filter(start_date__gt=timezone.now())
                        elif value == "cancelled":
                            queryset = queryset.filter(active=False)
                        else:
                            raise ValueError("Invalid value for 'search' parameter")
                    else:
                        field_lookup = f"{key}__icontains"
                        if not queryset.filter(**{field_lookup: value}).exists():
                            raise ValueError(
                                f"No events found with {key} containing {value}"
                            )
                        query &= Q(**{field_lookup: value})
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            if query:
                queryset = queryset.filter(query)

        return queryset

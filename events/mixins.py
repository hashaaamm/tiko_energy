from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response


class QuerysetFilterMixin:
    """
    Mixin for queryset with filters provided by params.
    """

    def filter_queryset(self, queryset):
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

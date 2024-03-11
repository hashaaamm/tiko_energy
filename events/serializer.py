from rest_framework import serializers
from django.utils import timezone
from .models import Event


class EventCreateSerializer(serializers.ModelSerializer):
    def validate(self, data):
        """
        Validate start_date and end_date are in the future,
        and end_date is greater than start_date.
        """

        current_time = timezone.now() - timezone.timedelta(seconds=1)
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if start_date < current_time:
            raise serializers.ValidationError(
                {"start_date": "Start date must be in the future."}
            )

        if end_date <= start_date:
            raise serializers.ValidationError(
                {"end_date": "End date must be greater than start date."}
            )

        return data

    class Meta:
        model = Event
        fields = [
            "name",
            "owner",
            "description",
            "start_date",
            "end_date",
            "event_type",
        ]


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "name",
            "owner",
            "description",
            "start_date",
            "end_date",
            "event_type",
            "created_date",
            "updated_date",
            "status",
            "number_of_attendees",
        ]

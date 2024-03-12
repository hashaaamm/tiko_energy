from rest_framework import serializers
from django.utils import timezone
from .models import Event


class EventListCreateSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    created_date = serializers.ReadOnlyField()
    updated_date = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()
    number_of_attendees = serializers.ReadOnlyField()

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

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["owner"] = user
        instance = super().create(validated_data)
        return instance

    class Meta:
        model = Event
        fields = [
            "id",
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


class EventDetailUpdateSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    list_of_attendees = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    number_of_attendees = serializers.ReadOnlyField
    created_date = serializers.ReadOnlyField()
    updated_date = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()

    def validate(self, data):
        """
        Validate start_date and end_date are in the future,
        and end_date is greater than start_date.
        """

        start_date = data.get("start_date")
        end_date = data.get("end_date")

        instance = self.instance

        if start_date:
            current_time = timezone.now() - timezone.timedelta(seconds=1)
            if start_date < current_time:
                raise serializers.ValidationError(
                    {"start_date": "Start date must be in the future."}
                )
        else:
            start_date = instance.start_date

        if end_date:
            if end_date <= start_date:
                raise serializers.ValidationError(
                    {"end_date": "End date must be greater than start date."}
                )
        else:
            end_date = instance.end_date

        data["start_date"] = start_date
        data["end_date"] = end_date

        return data

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "owner",
            "description",
            "start_date",
            "end_date",
            "event_type",
            "list_of_attendees",
            "created_date",
            "updated_date",
            "status",
            "number_of_attendees",
            "active",
        ]


class EventSubscribeSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        user = self.context["request"].user
        success = False

        if "/subscribe" in self.context["request"].path:

            if user not in instance.list_of_attendees.all():
                instance.list_of_attendees.add(user)
                message = "Subscribed to the event"
                success = True
            else:
                message = "Already Subscribed"
        elif "/unsubscribe" in self.context["request"].path:
            if user in instance.list_of_attendees.all():
                instance.list_of_attendees.remove(user)
                message = "Unsubscribed from the event"
                success = True

            else:
                message = "Already Unsubscribed"

        instance.save()
        return {"message": message, "success": success}

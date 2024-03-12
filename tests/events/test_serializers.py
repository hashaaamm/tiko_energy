import pytest
from events.serializers import (
    EventListCreateSerializer,
    EventDetailSerializer,
    EventUpdateSerializer,
    EventSubscribeSerializer,
)
from django.contrib.auth import get_user_model
from django.utils import timezone
from ..error_messages import REQUIRED_ERROR
from events.models import Event
from django.utils.dateparse import parse_datetime
from django.http import HttpRequest

User = get_user_model()


@pytest.mark.django_db
def test_event_create_serializer_with_valid_data(valid_user):
    request = HttpRequest()
    request.user = valid_user
    serializer = EventListCreateSerializer(
        data={
            "name": "Wine tasting",
            "description": "Try wines from all over Portugal",
            "start_date": timezone.now(),
            "end_date": timezone.now() + timezone.timedelta(hours=5),
            "event_type": "Meeting",
        },
        context={"request": request},
    )
    assert serializer.is_valid()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload, field, expected_errors",
    [
        [
            {
                "name": "Wine tasting",
                "description": "Try wines from all over Portugal",
                "start_date": timezone.now() - +timezone.timedelta(hours=5),
                "end_date": timezone.now() + timezone.timedelta(hours=5),
                "event_type": "Meeting",
            },
            "start_date",
            "Start date must be in the future.",
        ],
        [
            {
                "name": "Wine tasting",
                "description": "Try wines from all over Portugal",
                "start_date": timezone.now(),
                "end_date": timezone.now() - timezone.timedelta(hours=5),
                "event_type": "Meeting",
            },
            "end_date",
            "End date must be greater than start date.",
        ],
    ],
)
def test_event_create_serializer_with_invalid_date(
    valid_user, payload, field, expected_errors
):
    """Test serializer using invalid date"""
    # payload["owner"] = valid_user.pk
    request = HttpRequest()
    request.user = valid_user
    serializer = EventListCreateSerializer(
        data=payload,
        context={"request": request},
    )

    assert not serializer.is_valid()
    assert serializer.errors[field][0] == expected_errors


@pytest.mark.django_db
def test_event_create_serializer_with_invalid_data(valid_user):

    serializer = EventListCreateSerializer(data={})
    assert not serializer.is_valid()


@pytest.mark.django_db
def test_event_list_serializer(valid_user):
    name = "Wine tasting"
    owner = valid_user
    description = "Try wines from all over Portugal"
    start_date = timezone.now()
    end_date = timezone.now() + timezone.timedelta(hours=5)
    event_type = "Meeting"
    Event.objects.create(
        name=name,
        owner=owner,
        description=description,
        start_date=start_date,
        end_date=end_date,
        event_type=event_type,
    )
    all_events = Event.objects.all()
    serializer = EventListCreateSerializer(all_events, many=True)
    data = serializer.data[0]
    assert data["name"] == name
    assert data["owner"] == owner.pk
    assert data["description"] == description
    assert parse_datetime(data["start_date"]) == start_date
    assert parse_datetime(data["end_date"]) == end_date
    assert data["event_type"] == event_type
    assert data["number_of_attendees"] == 0


@pytest.mark.django_db
def test_event_detail_serializer(valid_user):
    name = "Wine tasting"
    owner = valid_user
    description = "Try wines from all over Portugal"
    start_date = timezone.now()
    end_date = timezone.now() + timezone.timedelta(hours=5)
    event_type = "Meeting"
    event = Event.objects.create(
        name=name,
        owner=owner,
        description=description,
        start_date=start_date,
        end_date=end_date,
        event_type=event_type,
    )
    event.list_of_attendees.set([valid_user])
    serializer = EventDetailSerializer(event)
    data = serializer.data
    assert data["name"] == name
    assert data["owner"] == owner.pk
    assert data["description"] == description
    assert parse_datetime(data["start_date"]) == start_date
    assert parse_datetime(data["end_date"]) == end_date
    assert data["event_type"] == event_type
    assert data["list_of_attendees"] == [valid_user.pk]
    assert data["created_date"]
    assert data["updated_date"]
    assert data["status"]
    assert data["number_of_attendees"] == 1


@pytest.mark.django_db
def test_event_update_serializer(valid_user):
    name = "Wine tasting"
    owner = valid_user
    description = "Try wines from all over Portugal"
    start_date = timezone.now()
    end_date = timezone.now() + timezone.timedelta(hours=5)
    event_type = "Meeting"
    event = Event.objects.create(
        name=name,
        owner=owner,
        description=description,
        start_date=start_date,
        end_date=end_date,
        event_type=event_type,
    )
    instance = Event.objects.first()
    serializer = EventUpdateSerializer(
        instance,
        data={
            "name": "New event name",
        },
        partial=True,
    )
    assert serializer.is_valid(), serializer.errors
    serializer.save()

    assert Event.objects.count() == 1
    assert Event.objects.first().name == "New event name"


@pytest.mark.django_db
def test_event_subscribe_serializer(valid_user):
    name = "Wine tasting"
    owner = valid_user
    description = "Try wines from all over Portugal"
    start_date = timezone.now()
    end_date = timezone.now() + timezone.timedelta(hours=5)
    event_type = "Meeting"
    event = Event.objects.create(
        name=name,
        owner=owner,
        description=description,
        start_date=start_date,
        end_date=end_date,
        event_type=event_type,
    )
    instance = Event.objects.first()
    request = HttpRequest()
    request.user = valid_user
    serializer = EventSubscribeSerializer(
        instance, data={"subscribe": True}, context={"request": request}
    )
    assert serializer.is_valid()
    assert serializer.save()

    assert instance.list_of_attendees.first().pk == valid_user.pk

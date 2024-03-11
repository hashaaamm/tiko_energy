import pytest
from events.serializer import EventCreateSerializer, EventListSerializer
from django.contrib.auth import get_user_model
from django.utils import timezone
from ..error_messages import REQUIRED_ERROR
from events.models import Event
from django.utils.dateparse import parse_datetime

User = get_user_model()


@pytest.mark.django_db
def test_event_create_serializer_with_valid_data(valid_user):

    serializer = EventCreateSerializer(
        data={
            "name": "Wine tasting",
            "owner": valid_user.pk,
            "description": "Try wines from all over Portugal",
            "start_date": timezone.now(),
            "end_date": timezone.now() + timezone.timedelta(hours=5),
            "event_type": "Meeting",
        }
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
    """Test serializer using invalid data"""
    payload["owner"] = valid_user.pk
    serializer = EventCreateSerializer(data=payload)

    assert not serializer.is_valid()
    assert serializer.errors[field][0] == expected_errors


@pytest.mark.django_db
def test_event_create_serializer_with_invalid_data(valid_user):

    serializer = EventCreateSerializer(data={})
    assert not serializer.is_valid()


@pytest.mark.django_db
def test_event_create_serializer_with_no_owner(valid_user):

    serializer = EventCreateSerializer(
        data={
            "name": "Wine tasting",
            "description": "Try wines from all over Portugal",
            "start_date": timezone.now(),
            "end_date": timezone.now() + timezone.timedelta(hours=5),
            "event_type": "Meeting",
        }
    )
    assert not serializer.is_valid()
    assert serializer.errors["owner"][0] == REQUIRED_ERROR


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
    serializer = EventListSerializer(all_events, many=True)
    data = serializer.data[0]
    assert data["name"] == name
    assert data["owner"] == owner.pk
    assert data["description"] == description
    assert parse_datetime(data["start_date"]) == start_date
    assert parse_datetime(data["end_date"]) == end_date
    assert data["event_type"] == event_type
    assert data["number_of_attendees"] == 0

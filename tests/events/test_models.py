import pytest
from django.utils import timezone

from events.models import Event
from users.models import CustomUser


@pytest.mark.django_db
def test_events_model(create_user):
    email = "john@gmail.com"
    password = "sdadfad3sd"
    user = CustomUser(email=email, password=password)
    user.save()

    name = "Wine tasting"
    owner = user
    description = "Try wines from all over Portugal"
    start_date = timezone.now()
    end_date = start_date + timezone.timedelta(hours=5)
    event_type = " Meeting"
    maximum_attendees = 10
    events = Event(
        name=name,
        owner=owner,
        description=description,
        start_date=start_date,
        end_date=end_date,
        event_type=event_type,
        maximum_attendees=maximum_attendees,
    )
    events.save()
    assert events.name == name
    assert events.owner == owner
    assert events.description == description
    assert events.start_date == start_date
    assert events.end_date == end_date
    assert events.event_type == event_type
    assert events.maximum_attendees == maximum_attendees
    assert events.active
    assert events.status
    assert not events.list_of_attendees.exists()
    assert events.created_date
    assert events.updated_date

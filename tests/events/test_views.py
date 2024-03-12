import pytest
from rest_framework import status
from django.utils import timezone
from django.urls import reverse
from django.utils.dateparse import parse_datetime


valid_payload = {
    "name": "Wine tasting",
    "description": "Try wines from all over Portugal",
    "start_date": timezone.now() + timezone.timedelta(hours=1),
    "end_date": timezone.now() + timezone.timedelta(hours=5),
    "event_type": "Meeting",
}


@pytest.fixture
def event_create_with_login(client_with_credentials):
    """Return api client instance with valid credentials for making authorized request"""

    def _event_create_with_login(payload=valid_payload):

        url = reverse("events-list-create")
        response = client_with_credentials.post(
            url,
            data=payload,
            format="json",
        )
        return response

    return _event_create_with_login


@pytest.mark.django_db
def test_event_create_with_valid_data(event_create_with_login):
    """Test create event with the valid data and auth credentials"""
    response = event_create_with_login()
    data = response.data
    assert response.status_code == status.HTTP_201_CREATED
    assert data["id"]
    assert data["owner"]
    assert data["name"] == valid_payload["name"]
    assert data["description"] == valid_payload["description"]
    assert parse_datetime(data["start_date"]) == valid_payload["start_date"]
    assert parse_datetime(data["end_date"]) == valid_payload["end_date"]
    assert data["event_type"] == valid_payload["event_type"]


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
def test_event_create_with_invalid_date(
    event_create_with_login, payload, field, expected_errors
):
    """Test create event using invalid DATE and auth credentials"""
    response = event_create_with_login(payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data[field][0] == expected_errors


@pytest.mark.django_db
def test_event_create_with_invalid_data(event_create_with_login):
    """Test create event using invalid DATA and auth credentials"""
    response = event_create_with_login({})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_event_create_without_login(api_client):
    """Test create event without auth credentials"""
    url = reverse("events-list-create")
    response = api_client.post(url, data=valid_payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_event_list(api_client, event_create_with_login):
    """Test event list without auth credentials"""
    # create events before getting the list
    event_create_with_login()
    event_create_with_login()

    url = reverse("events-list-create")
    response = api_client.get(url)
    # we are not testing the format for now, this might be required in production
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_event_details(api_client, event_create_with_login):
    event = event_create_with_login()
    url = reverse("events-detail-update", kwargs={"pk": event.data["id"]})
    response = api_client.get(url)
    data = response.data

    assert response.status_code == status.HTTP_200_OK

    assert data["id"]
    assert data["owner"]
    assert data["name"] == valid_payload["name"]
    assert data["description"] == valid_payload["description"]
    assert parse_datetime(data["start_date"]) == valid_payload["start_date"]
    assert parse_datetime(data["end_date"]) == valid_payload["end_date"]
    assert data["event_type"] == valid_payload["event_type"]
    assert data["list_of_attendees"] == []
    assert data["created_date"]
    assert data["updated_date"]
    assert data["status"]


@pytest.mark.django_db
def test_event_update(client_with_credentials, event_create_with_login):
    event = event_create_with_login()
    url = reverse("events-detail-update", kwargs={"pk": event.data["id"]})
    response = client_with_credentials.get(url)
    assert response.status_code == status.HTTP_200_OK

    payload = {
        "name": "updated name",
        "description": "updated description",
        "start_date": "2026-03-15T10:00:00Z",
        "end_date": "2027-03-15T15:00:00Z",
        "event_type": "updated type",
        "active": False,
    }
    update_response = client_with_credentials.put(
        url,
        data=payload,
        format="json",
    )
    assert update_response.status_code == status.HTTP_200_OK
    data = update_response.data
    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]
    assert data["start_date"] == payload["start_date"]
    assert data["end_date"] == payload["end_date"]
    assert data["event_type"] == payload["event_type"]
    assert data["active"] == payload["active"]

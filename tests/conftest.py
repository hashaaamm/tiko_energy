import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def valid_payload():
    return {"email": "jhon@example.com", "password": "asuh9898hs"}


@pytest.fixture
def create_user(api_client, valid_payload):

    def _create_user(payload=valid_payload):
        """
        There is no basename in djoser urls.py, therefore url will be derived from the model
        our user model is called "CustomUser"
        By default we will use valid_payload
        """
        url = reverse("customuser-list")
        response = api_client.post(url, payload, format="json")
        return response

    return _create_user

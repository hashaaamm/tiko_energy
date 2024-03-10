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
        return api_client.post(url, payload, format="json")

    return _create_user


@pytest.fixture
def login_user(api_client, create_user, valid_payload):
    def _login_user(payload=valid_payload):
        create_user()
        url = reverse("jwt-create")
        response = api_client.post(url, payload, format="json")
        return response

    return _login_user


@pytest.fixture
def refresh_token(api_client, login_user):

    def _refresh_token(payload):
        url = reverse("jwt-refresh")
        return api_client.post(url, payload, format="json")

    return _refresh_token

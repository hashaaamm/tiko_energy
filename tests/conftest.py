import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def valid_payload():
    return {"email": "jhon@example.com", "password": "asuh9898hs"}


@pytest.fixture
def valid_user():
    return User.objects.create_user(email="test123@example.com", password="asuh9898hs")


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
def refresh_token(api_client):

    def _refresh_token(payload):
        url = reverse("jwt-refresh")
        return api_client.post(url, payload, format="json")

    return _refresh_token


@pytest.fixture
def verify_token(api_client):
    def _verify_token(payload):
        url = reverse("jwt-verify")
        return api_client.post(url, payload, format="json")

    return _verify_token


@pytest.fixture
def client_with_credentials(login_user):
    response_login_user = login_user()
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'JWT {response_login_user.data["access"]}')
    return client

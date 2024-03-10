import pytest
from rest_framework import status
from ..error_messages import REQUIRED_ERROR
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_create_user_with_valid_data(create_user, valid_payload):
    """Test user creation with Valid Data"""
    response = create_user()
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.data
    assert response.data["email"] == valid_payload["email"]


@pytest.mark.django_db
def test_create_user_with_non_unique_email(create_user):
    """Test user creation with email already exits"""

    # Create user
    response = create_user()
    assert response.status_code == status.HTTP_201_CREATED

    # Recreate user
    response = create_user()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["email"] == [
        "custom user with this email address already exists."
    ]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "create_user, payload, expected_errors, status_code",
    [
        [
            "create_user",
            {},
            {
                "email": [REQUIRED_ERROR],
                "password": [REQUIRED_ERROR],
            },
            status.HTTP_400_BAD_REQUEST,
        ],
        [
            "create_user",
            {"password": "testpassword"},
            {"email": [REQUIRED_ERROR]},
            status.HTTP_400_BAD_REQUEST,
        ],
        [
            "create_user",
            {"email": "test", "password": "testpassword"},
            {"email": ["Enter a valid email address."]},
            status.HTTP_400_BAD_REQUEST,
        ],
        [
            "create_user",
            {"email": "test@example.com"},
            {"password": [REQUIRED_ERROR]},
            status.HTTP_400_BAD_REQUEST,
        ],
    ],
    indirect=["create_user"],
)
def test_create_user_invalid_json(create_user, payload, expected_errors, status_code):
    """Test user creation with Invalid Data"""
    response = create_user(payload)
    assert response.status_code == status_code
    assert response.data == expected_errors

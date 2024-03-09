import pytest
from rest_framework import status
from ..error_messages import REQUIRED_ERROR, INVALID_CREDENTIALS_ERROR


@pytest.mark.django_db
def test_login_with_valid_data(login_user, valid_payload):
    """Test user Login with Valid credentials"""
    response = login_user()
    assert response.status_code == status.HTTP_200_OK
    assert response.data["access"]
    assert response.data["refresh"]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "login_user, payload, expected_errors, status_code",
    [
        [
            "login_user",
            {},
            {
                "email": [REQUIRED_ERROR],
                "password": [REQUIRED_ERROR],
            },
            status.HTTP_400_BAD_REQUEST,
        ],
        [
            "login_user",
            {"password": "testpassword"},
            {"email": [REQUIRED_ERROR]},
            status.HTTP_400_BAD_REQUEST,
        ],
        [
            "login_user",
            {"email": "test@example.com"},
            {"password": [REQUIRED_ERROR]},
            status.HTTP_400_BAD_REQUEST,
        ],
        [
            "login_user",
            {"email": "wrong_email", "password": "testpassword"},
            {"detail": INVALID_CREDENTIALS_ERROR},
            status.HTTP_401_UNAUTHORIZED,
        ],
        [
            "login_user",
            {"email": "wrong_email", "password": "wrong_password"},
            {"detail": INVALID_CREDENTIALS_ERROR},
            status.HTTP_401_UNAUTHORIZED,
        ],
    ],
    indirect=["login_user"],
)
def test_login_with_invalid_data(login_user, payload, expected_errors, status_code):
    """Test user Login with Invalid credentials"""
    response = login_user(payload)
    assert response.status_code == status_code
    assert response.data == expected_errors

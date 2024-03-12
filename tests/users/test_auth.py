import pytest
from rest_framework import status

from ..error_messages import INVALID_CREDENTIALS_ERROR, REQUIRED_ERROR


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


@pytest.mark.django_db
def test_refresh_token_valid_data(login_user, refresh_token):
    """Test refresh token with valid refresh token"""
    response_login_user = login_user()
    assert response_login_user.status_code == status.HTTP_200_OK

    response_refresh_token = refresh_token(
        {"refresh": response_login_user.data["refresh"]}
    )
    assert response_refresh_token.status_code == status.HTTP_200_OK
    assert response_refresh_token.data["access"]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "refresh_token, payload, expected_errors, status_code",
    [
        [
            "refresh_token",
            {},
            {
                "refresh": [REQUIRED_ERROR],
            },
            status.HTTP_400_BAD_REQUEST,
        ],
        [
            "refresh_token",
            {"refresh": "fake_token"},
            {"detail": "Token is invalid or expired", "code": "token_not_valid"},
            status.HTTP_401_UNAUTHORIZED,
        ],
    ],
    indirect=["refresh_token"],
)
@pytest.mark.django_db
def test_refresh_token_invalid_data(
    refresh_token, payload, expected_errors, status_code
):
    """Test refresh token with invalid data"""
    response = refresh_token(payload)
    assert response.status_code == status_code
    assert response.data == expected_errors


@pytest.mark.django_db
def test_verify_token_valid_data(login_user, verify_token):
    """Test verify token using a valid access token"""
    response_login_user = login_user()
    assert response_login_user.status_code == status.HTTP_200_OK

    response_verify_token = verify_token({"token": response_login_user.data["access"]})
    assert response_verify_token.status_code == status.HTTP_200_OK


pytest.mark.django_db


@pytest.mark.parametrize(
    "verify_token, payload, expected_errors, status_code",
    [
        [
            "verify_token",
            {},
            {
                "token": [REQUIRED_ERROR],
            },
            status.HTTP_400_BAD_REQUEST,
        ],
        [
            "verify_token",
            {"token": "fake_token"},
            {"detail": "Token is invalid or expired", "code": "token_not_valid"},
            status.HTTP_401_UNAUTHORIZED,
        ],
    ],
    indirect=["verify_token"],
)
@pytest.mark.django_db
def test_verify_token_invalid_data(verify_token, payload, expected_errors, status_code):
    """Test verify token using a invalid access token"""
    response = verify_token(payload)
    assert response.status_code == status_code
    assert response.data == expected_errors

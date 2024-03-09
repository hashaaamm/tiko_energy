import pytest
from rest_framework import status


@pytest.mark.django_db
def test_create_user(create_user, valid_payload):
    response = create_user()
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.data
    assert response.data["email"] == valid_payload["email"]


@pytest.mark.django_db
def test_create_user_with_non_unique_email(create_user):

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
                "email": ["This field is required."],
                "password": ["This field is required."],
            },
            400,
        ],
        [
            "create_user",
            {"password": "testpassword"},
            {"email": ["This field is required."]},
            400,
        ],
        [
            "create_user",
            {"email": "test", "password": "testpassword"},
            {"email": ["Enter a valid email address."]},
            400,
        ],
        [
            "create_user",
            {"email": "test@example.com"},
            {"password": ["This field is required."]},
            400,
        ],
    ],
    indirect=["create_user"],
)
def test_create_user_invalid_json(create_user, payload, expected_errors, status_code):
    response = create_user(payload)
    assert response.status_code == status_code
    assert response.data == expected_errors

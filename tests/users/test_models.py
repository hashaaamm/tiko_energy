import pytest

from users.models import CustomUser


@pytest.mark.django_db
def test_custom_user_model():
    email = "john@gmail.com"
    password = "sdadfad3sd"
    user = CustomUser(email=email, password=password)
    user.save()
    assert user.email == email
    assert user.password == password
    assert not user.is_admin
    assert not user.is_staff

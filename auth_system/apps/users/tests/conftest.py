import pytest
from rest_framework.test import APIClient

from apps.users.models import User, Session, AccessRoleRule, Role, BusinessElement


@pytest.fixture
def regular_user():
    user = User.objects.create_user(
        email='user@example.com',
        username='viktor8',
        password='testpass123',
        first_name='Viktor',
        last_name='Volkov',
        is_active=True
    )
    return user


@pytest.fixture
def admin_user():
    user = User.objects.create_user(
        email='admin@example.com',
        username='admin',
        password='adminpass123',
        first_name='Admin',
        last_name='Adminov',
        is_staff=True,
        is_superuser=True,
        is_active=True,
        role=Role.objects.get(name='Администратор')
    )
    return user


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_registration_data():
    return {
        'email': 'viktor@mail.ru',
        'username': 'viktor8',
        'password': 'newpassword123',
        'password_repeat': 'newpassword123',
        'first_name': 'Viktor',
        'last_name': 'Volkov'
    }


@pytest.fixture
def user_session(regular_user):
    session = Session.create_session(regular_user)
    return session


@pytest.fixture
def admin_session(admin_user):
    session = Session.create_session(admin_user)
    return session


@pytest.fixture
def element():
    return BusinessElement.objects.create(
        name='Товары'
    )


@pytest.fixture
def access_rule(element):
    return AccessRoleRule.objects.create(
        role=Role.objects.get(name='Пользователь'),
        element=element
    )

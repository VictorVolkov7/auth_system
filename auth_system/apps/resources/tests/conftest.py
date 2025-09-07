import pytest
from rest_framework.test import APIClient

from apps.users.models import BusinessElement, AccessRoleRule, Role, User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def element():
    return BusinessElement.objects.create(name='Товары', description='Продукты')


@pytest.fixture
def users():
    roles = Role.objects.all()
    u1 = User.objects.create_user(
        username='Ivan2000', email='ivanov@mail.ru', password='testpass123', role=roles[0], is_active=True
    )
    u2 = User.objects.create_user(
        username='admin', email='admin@mail.ru', password='testpass123', role=roles[1], is_active=True
    )
    u3 = User.objects.create_user(
        username='Maksim8', email='maksimov@example.com', password='testpass123', role=roles[2], is_active=True
    )
    return u1, u2, u3


@pytest.fixture
def access_rules(element):
    roles = Role.objects.all()
    rules = [
        AccessRoleRule.objects.create(role=roles[0], element=element,
                                      read_permission=True, read_all_permission=False,
                                      create_permission=True, update_permission=True, update_all_permission=False,
                                      delete_permission=True, delete_all_permission=False),
        AccessRoleRule.objects.create(role=roles[1], element=element,
                                      read_permission=True, read_all_permission=True,
                                      create_permission=False, update_permission=True, update_all_permission=True,
                                      delete_permission=True, delete_all_permission=True),
        AccessRoleRule.objects.create(role=roles[2], element=element,
                                      read_permission=True, read_all_permission=True,
                                      create_permission=True, update_permission=True, update_all_permission=True,
                                      delete_permission=True, delete_all_permission=False),
    ]
    return rules

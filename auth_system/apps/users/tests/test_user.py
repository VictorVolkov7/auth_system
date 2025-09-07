import pytest
from django.urls import reverse
from rest_framework import status
from apps.users.models import User, AccessRoleRule, Role


@pytest.mark.django_db
def test_user_registration(api_client, user_registration_data):
    response = api_client.post(reverse('users:user-register'), user_registration_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(email=user_registration_data.get('email')).exists()


@pytest.mark.django_db
def test_invalid_user_registration(api_client, user_registration_data):
    user_registration_data['password_repeat'] = '1212'

    response = api_client.post(reverse('users:user-register'), user_registration_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Passwords do not match" in response.data['non_field_errors']


@pytest.mark.django_db
def test_user_login(api_client, regular_user):
    data = {'email': regular_user.email, 'password': 'testpass123'}

    response = api_client.post(reverse('users:user-login'), data)

    assert response.status_code == status.HTTP_200_OK
    assert 'session_key' in response.cookies


@pytest.mark.django_db
def test_user_login_invalid_credentials(api_client):
    data = {'email': 'wrong@gmail.com', 'password': 'wrongpass'}

    response = api_client.post(reverse('users:user-login'), data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_user_logout(api_client, user_session):
    api_client.cookies['session_key'] = user_session.session_key

    response = api_client.post(reverse('users:user-logout'))

    assert response.status_code == 200
    user_session.refresh_from_db()
    assert not user_session.is_active
    cookie = response.cookies.get('session_key')
    assert cookie is not None
    assert cookie.value == ''
    assert cookie['max-age'] == 0


@pytest.mark.django_db
def test_get_user_profile(api_client, regular_user, user_session):
    api_client.cookies['session_key'] = user_session.session_key

    response = api_client.get(reverse('users:user-profile'))

    assert response.status_code == status.HTTP_200_OK
    assert response.data['email'] == regular_user.email


@pytest.mark.django_db
def test_update_user_profile(api_client, regular_user, user_session):
    api_client.cookies['session_key'] = user_session.session_key
    data = {'first_name': 'UpdatedName'}

    response = api_client.patch(reverse('users:user-profile'), data)

    assert response.status_code == status.HTTP_200_OK
    regular_user.refresh_from_db()
    assert regular_user.first_name == 'UpdatedName'


@pytest.mark.django_db
def test_deactivate_user_profile(api_client, regular_user, user_session):
    api_client.cookies['session_key'] = user_session.session_key

    response = api_client.delete(reverse('users:user-profile'))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    regular_user.refresh_from_db()
    assert not regular_user.is_active


@pytest.mark.django_db
@pytest.mark.parametrize('role, status_result', [
    ('Администратор', status.HTTP_200_OK),
    ('Пользователь', status.HTTP_403_FORBIDDEN),
])
def test_list_access_rules(api_client, admin_user, access_rule, admin_session, role, status_result):
    user_role = Role.objects.get(name=role)
    admin_user.role = user_role
    admin_user.save()
    api_client.cookies['session_key'] = admin_session.session_key

    response = api_client.get(reverse('users:access_rule_list'))

    assert response.status_code == status_result

    if response.status_code == status.HTTP_200_OK:
        assert len(response.data) == AccessRoleRule.objects.count()
    else:
        assert 'У вас недостаточно прав для выполнения данного действия.' in response.data['detail']


@pytest.mark.django_db
@pytest.mark.parametrize('role, status_result', [
    ('Администратор', status.HTTP_200_OK),
    ('Пользователь', status.HTTP_403_FORBIDDEN),
])
def test_access_rule_detail_update(api_client, admin_user, access_rule, admin_session, role, status_result):
    user_role = Role.objects.get(name=role)
    admin_user.role = user_role
    admin_user.save()
    api_client.cookies['session_key'] = admin_session.session_key
    data = {'read_permission': True}

    response = api_client.patch(reverse('users:access_rule_detail', args=[access_rule.id]), data)

    assert response.status_code == status_result
    access_rule.refresh_from_db()
    if response.status_code == status.HTTP_200_OK:
        assert access_rule.read_permission is True
    else:
        assert 'У вас недостаточно прав для выполнения данного действия.' in response.data['detail']


@pytest.mark.django_db
@pytest.mark.parametrize('role, status_result', [
    ('Администратор', status.HTTP_204_NO_CONTENT),
    ('Пользователь', status.HTTP_403_FORBIDDEN),
])
def test_access_rule_detail_delete(api_client, admin_user, access_rule, admin_session, role, status_result):
    user_role = Role.objects.get(name=role)
    admin_user.role = user_role
    admin_user.save()
    api_client.cookies['session_key'] = admin_session.session_key

    response = api_client.delete(reverse('users:access_rule_detail', args=[access_rule.id]))

    assert response.status_code == status_result
    if response.status_code == status.HTTP_204_NO_CONTENT:
        assert not AccessRoleRule.objects.filter(id=access_rule.id).exists()
    else:
        assert 'У вас недостаточно прав для выполнения данного действия.' in response.data['detail']

import pytest
from django.urls import reverse
from rest_framework import status

from apps.resources.views import PRODUCTS


@pytest.fixture(autouse=True)
def reset_products(users):
    PRODUCTS.clear()
    PRODUCTS.extend([
        {'id': 1, 'name': 'Apple', 'owner': users[0].id},
        {'id': 2, 'name': 'Orange', 'owner': users[2].id},
        {'id': 3, 'name': 'Banana', 'owner': users[0].id},
    ])


@pytest.mark.django_db
@pytest.mark.parametrize('user_idx, expected_count', [
    (0, 2),
    (1, 3),
    (2, 3),
])
def test_product_list(api_client, access_rules, users, user_idx, expected_count):
    api_client.force_authenticate(user=users[user_idx])

    response = api_client.get(reverse('resources:products'))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == expected_count


@pytest.mark.django_db
@pytest.mark.parametrize('user_idx, can_create', [
    (0, True),
    (1, False),
    (2, True),
])
def test_product_create(api_client, access_rules, users, user_idx, can_create):
    api_client.force_authenticate(user=users[user_idx])

    response = api_client.post(reverse('resources:products'), data={'name': 'Cherry'})

    if can_create:
        assert response.status_code == status.HTTP_201_CREATED or response.status_code == status.HTTP_200_OK
        assert response.data['owner'] == users[user_idx].id
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
@pytest.mark.parametrize('user_idx, target_product, expected_status', [
    (0, 1, status.HTTP_200_OK),
    (0, 2, status.HTTP_403_FORBIDDEN),
    (1, 1, status.HTTP_200_OK),
    (2, 1, status.HTTP_200_OK),
])
def test_product_update(api_client, access_rules, users, user_idx, target_product, expected_status):
    api_client.force_authenticate(user=users[user_idx])

    response = api_client.patch(reverse('resources:product-detail', args=[target_product]),
                                data={'name': 'Updated'})

    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize('user_idx, target_product, expected_status', [
    (0, 1, status.HTTP_204_NO_CONTENT),
    (0, 2, status.HTTP_403_FORBIDDEN),
    (1, 2, status.HTTP_204_NO_CONTENT),
    (2, 2, status.HTTP_204_NO_CONTENT),
])
def test_product_delete(api_client, access_rules, users, user_idx, target_product, expected_status):
    api_client.force_authenticate(user=users[user_idx])

    response = api_client.delete(reverse('resources:product-detail', args=[target_product]))

    assert response.status_code == expected_status

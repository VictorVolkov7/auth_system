from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from apps.resources.serializers import ProductSerializer
from apps.users.models import BusinessElement, AccessRoleRule
from apps.users.permissions import RoleBasedPermission

PRODUCTS = [
    {'id': 1, 'name': 'Apple', 'owner': 1},
    {'id': 2, 'name': 'Orange', 'owner': 3},
    {'id': 3, 'name': 'Banana', 'owner': 1},
]


class ProductListView(generics.ListCreateAPIView):
    """API view to list all products or create a new product."""
    permission_classes = [IsAuthenticated, RoleBasedPermission]
    business_element_name = 'Товары'
    serializer_class = ProductSerializer

    def get_queryset(self):
        """Returns the list of products accessible to the requesting user based on their role permissions."""
        element = BusinessElement.objects.get(name=self.business_element_name)
        rule = AccessRoleRule.objects.get(role=self.request.user.role, element=element)

        if rule.read_all_permission:
            return PRODUCTS
        elif rule.read_permission:
            return [p for p in PRODUCTS if p['owner'] == self.request.user.id]
        return []

    def perform_create(self, serializer=None):
        """Creates a new product with the given name and assigns ownership to the requesting user."""
        new_product = {
            'id': len(PRODUCTS) + 1,
            'name': self.request.data.get('name'),
            'owner': self.request.user.id
        }
        PRODUCTS.append(new_product)
        serializer.instance = new_product


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """API view to retrieve, update, or delete a specific product by its ID."""
    permission_classes = [IsAuthenticated, RoleBasedPermission]
    business_element_name = 'Товары'
    serializer_class = ProductSerializer

    def get_object(self, serializer=None):
        """Retrieves the product matching the given primary key (pk)."""
        try:
            pk = int(self.kwargs.get('pk'))
        except (TypeError, ValueError):
            raise NotFound('Invalid product ID')

        obj = next((p for p in PRODUCTS if p['id'] == pk), None)
        if not obj:
            raise NotFound('Not found')

        self.check_object_permissions(self.request, obj)
        return obj

    def perform_update(self, serializer=None):
        """Updates the product's name with the provided data."""
        obj = self.get_object()
        obj['name'] = self.request.data.get('name', obj['name'])
        serializer.instance = obj

    def perform_destroy(self, instance=None):
        """Deletes the product from the PRODUCTS list."""
        obj = self.get_object()
        PRODUCTS.remove(obj)

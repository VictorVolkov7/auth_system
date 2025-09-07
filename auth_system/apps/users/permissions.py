from rest_framework.permissions import BasePermission
from .models import BusinessElement, AccessRoleRule


class RoleBasedPermission(BasePermission):
    """Custom permission class for role-based access control."""

    action_map = {
        'GET': ('read_permission', 'read_all_permission'),
        'POST': ('create_permission', None),
        'PUT': ('update_permission', 'update_all_permission'),
        'PATCH': ('update_permission', 'update_all_permission'),
        'DELETE': ('delete_permission', 'delete_all_permission'),
    }

    @staticmethod
    def _get_rule(user, element_name):
        """
        Safely retrieves the AccessRoleRule instance for the given user and business element.

        Args:
            user: The user whose role is checked.
            element_name: The name of the business element.
        Returns:
            AccessRoleRule instance if found and user is authenticated with a role; otherwise None.
        """
        if not user.is_authenticated or not getattr(user, 'role', None):
            return None
        try:
            element = BusinessElement.objects.get(name=element_name)
            return AccessRoleRule.objects.get(role=user.role, element=element)
        except (BusinessElement.DoesNotExist, AccessRoleRule.DoesNotExist):
            return None

    def has_permission(self, request, view):
        """
        Checks if the user has general permission to perform the request method on the view.

        Args:
            request: The HTTP request object.
            view: The view being accessed.
        Returns:
            True if permission is granted, False otherwise.
        """
        element_name = getattr(view, 'business_element_name', None)
        rule = self._get_rule(request.user, element_name)
        if not rule:
            return False

        own_perm, all_perm = self.action_map.get(request.method, (None, None))

        if all_perm and getattr(rule, all_perm, False):
            return True

        if own_perm and getattr(rule, own_perm, False):
            return True

    def has_object_permission(self, request, view, obj):
        """
        Checks if the user has permission to perform the request method on a specific object.

        Args:
            request: The HTTP request object.
            view: The view being accessed.
            obj: The object being accessed.
        Returns:
            True if permission is granted, False otherwise.
        """
        element_name = getattr(view, 'business_element_name', None)
        rule = self._get_rule(request.user, element_name)
        if not rule:
            return False

        own_perm, all_perm = self.action_map.get(request.method, (None, None))

        if all_perm and getattr(rule, all_perm, False):
            return True

        if own_perm and getattr(rule, own_perm, False):
            owner_id = obj.get('owner') if isinstance(obj, dict) else getattr(obj, 'owner', None)
            return owner_id == request.user.id

        return False


class IsAdminUserRole(BasePermission):
    """Allows access only to users with the administrator role."""

    def has_permission(self, request, view):
        """
        Checks if the user has permission to access the view based on authentication and admin role.

        Args:
            request: The HTTP request object.
            view: The view being accessed.
        Returns:
            True if the user is authenticated and has the 'admin' role, False otherwise.
        """
        user = request.user
        return bool(user.is_authenticated and getattr(user.role, 'name', None) == 'Администратор')

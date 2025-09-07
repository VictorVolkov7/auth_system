from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

from apps.users.models import User, Session, AccessRoleRule
from apps.users.permissions import IsAdminUserRole
from apps.users.serializers import UserSerializer, UserCreateSerializer, AccessRoleRuleSerializer


class UserRegistrationView(generics.CreateAPIView):
    """
    API view for user registration.

    Allows creating a new user account. Uses UserCreateSerializer for validation and creation.
    """
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


class UserLoginView(generics.GenericAPIView):
    """
    API view for user login.

    Handles user authentication by email and password. If successful, creates a session and sets a cookie.
    """
    serializer_class = UserSerializer
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        """
        Authenticates the user and logs them in by creating a session.

        Args:
            request: The HTTP request object containing 'email' and 'password' in data.
        Returns:
            response: A success response with a session cookie if login succeeds, or an error response.
        """
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            return Response({'detail': _('Invalid credentials.')}, status=401)

        if not user.check_password(password):
            return Response({'detail': _('Invalid credentials.')}, status=401)

        Session.objects.filter(user=user, is_active=True).update(is_active=False)

        session = Session.create_session(user)
        response = Response({'detail': _('Logged in successfully.')})
        response.set_cookie('session_key', session.session_key, expires=session.expire_at, httponly=True,
                            secure=True, samesite='Lax')
        return response


class UserLogoutView(generics.GenericAPIView):
    """
    API view for user logout.

    Deactivates the user's active session and clears the session cookie.
    """
    http_method_names = ['post']
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Logs out the user by deactivating their session and deleting the cookie.

        Args:
            request: The HTTP request object.
        Returns:
            response: A success response indicating logout.
        """
        session_key = request.COOKIES.get('session_key')
        if session_key:
            Session.objects.filter(session_key=session_key, is_active=True).update(is_active=False)
        response = Response({'detail': _('Logged out successfully')})
        response.delete_cookie('session_key')
        return response


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for user profile management.

    Allows authenticated users to retrieve, update, or deactivate their profile.
    Deactivation sets the user as inactive and deactivates all their sessions.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Returns the current authenticated user as the object for the view.

        Returns:
            The authenticated user instance.
        """
        return self.request.user

    def perform_destroy(self, instance):
        """
         Deactivates the user and all their active sessions instead of deleting.

         Args:
             instance: The user instance to deactivate.
         """
        instance.is_active = False
        instance.save()

        instance.sessions.filter(is_active=True).update(is_active=False)

        response = Response({'detail': _('Account was delete.')}, status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('session_key')
        return response


class AccessRoleRuleListView(generics.ListAPIView):
    """API view for getting AccessRoleRule list."""
    queryset = AccessRoleRule.objects.all()
    serializer_class = AccessRoleRuleSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]


class AccessRoleRuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for AccessRoleRule instances.

    This view provides standard CRUD operations for AccessRoleRule objects, allowing
    authenticated admin users to manage access rules.
    """
    queryset = AccessRoleRule.objects.all()
    serializer_class = AccessRoleRuleSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]

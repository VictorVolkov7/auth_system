from rest_framework.authentication import BaseAuthentication

from apps.users.models import Session


class CookieSessionAuthentication(BaseAuthentication):
    """
    Custom DRF authentication class that trusts 'request.user' set by CustomSessionMiddleware.
    """

    def authenticate(self, request):
        """
        Custom DRF authentication class that authenticates users based on session cookies.

        Args:
            request: The HTTP request object.
        Returns:
            A tuple of (user, None) if authenticated, else None.
        """

        session_key = request.COOKIES.get('session_key')
        if not session_key:
            return None

        try:
            session = Session.objects.select_related('user').get(
                session_key=session_key,
                is_active=True
            )
            if session.is_expired() or not session.user.is_active:
                session.is_active = False
                session.save()
                return None
            return session.user, None
        except Session.DoesNotExist:
            return None

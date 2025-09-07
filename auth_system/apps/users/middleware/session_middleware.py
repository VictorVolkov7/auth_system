from django.contrib.auth.models import AnonymousUser

from apps.users.models import Session


class CustomSessionMiddleware:
    """Middleware for working with sessions via cookies."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/') or request.path.startswith('/static/'):
            return self.get_response(request)

        session_key = request.COOKIES.get('session_key')
        request.user = AnonymousUser()
        expired_session = None

        if session_key:
            try:
                session = Session.objects.select_related('user').get(
                    session_key=session_key,
                    is_active=True
                )
                if not session.is_expired() and session.user.is_active:
                    request.user = session.user
                else:
                    session.is_active = False
                    session.save()
                    expired_session = session_key
            except Session.DoesNotExist:
                pass

        response = self.get_response(request)

        if expired_session:
            response.delete_cookie('session_key')

        return response

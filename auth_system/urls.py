from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls', namespace='users')),
    path('', include('apps.resources.urls', namespace='resources')),

    # Documentation urls
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG and settings.USE_DEBUG_TOOLBAR:
    try:
        import debug_toolbar  # noqa
        urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
    except ModuleNotFoundError:
        pass

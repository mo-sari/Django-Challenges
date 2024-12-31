from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from drf_spectacular.views import (
     SpectacularAPIView,
     SpectacularRedocView,
     SpectacularSwaggerView)
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('rests/', include('restaurants.urls')),

    # swagger urls
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(
        url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'),
         name='redoc'),

] + debug_toolbar_urls()

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        # Other URLs for your app
    ]

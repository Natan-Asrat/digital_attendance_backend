from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("digital_attendance/admin/", admin.site.urls),
    path("digital_attendance/api/account/", include("account.urls")),
    path("digital_attendance/api/organization/", include("organization.urls")),
    path("digital_attendance/api/program/", include("program.urls")),
    path("digital_attendance/api/event/", include("event.urls")),
    path('digital_attendance/api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('digital_attendance/api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

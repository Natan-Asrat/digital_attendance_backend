from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrganizationViewset

router = DefaultRouter()
router.register(r'organizations', OrganizationViewset)

urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import path
from .views import roles

urlpatterns = [
    path('', roles, name='roles'),
]

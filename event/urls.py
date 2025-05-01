from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttendanceViewset, EventViewSet, NestedAttendanceViewset, NestedEventViewSet
from program.views import ProgramSimpleViewset
from rest_framework_nested import routers

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'attendance', AttendanceViewset)

event_router = routers.NestedDefaultRouter(router, r'events', lookup='event')
event_router.register(r'attendance', NestedAttendanceViewset, basename='event-attendance')


router.register(r'programs', ProgramSimpleViewset, basename='program')
program_router = routers.NestedDefaultRouter(router, r'programs', lookup='program')
program_router.register(r'events', NestedEventViewSet, basename='program-events')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(program_router.urls)),
    path('', include(event_router.urls))
]

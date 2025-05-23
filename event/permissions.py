from rest_framework.permissions import BasePermission
from organization.models import OrganizationAdmin
from program.models import ProgramEventAdmin, Program
from .models import Event

class EventViewSetPermissions(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        action = view.action

        # event_by_short_code allows any user (no authentication required)
        if action == 'event_by_short_code':
            return True

        # All other actions require authentication
        if not user or not user.is_authenticated:
            return False

        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        action = view.action

        # EventViewSet actions (archive_event, reactivate_event, conclude_event)
        program = obj.program
        organization = program.organization

        if action == 'conclude_event':
            return (
                organization.created_by == user or
                OrganizationAdmin.objects.filter(
                    user=user,
                    organization=organization,
                    is_active=True
                ).exists() or
                ProgramEventAdmin.objects.filter(
                    user=user,
                    program=program,
                    is_active=True,
                    can_conclude_events=True
                ).exists()
            )

        if action in ['archive_event', 'reactivate_event']:
            return (
                organization.created_by == user or
                OrganizationAdmin.objects.filter(
                    user=user,
                    organization=organization,
                    is_active=True
                ).exists() or
                ProgramEventAdmin.objects.filter(
                    user=user,
                    program=program,
                    is_active=True,
                    can_archive_event=True
                ).exists()
            )                
class NestedEventViewSetPermissions(BasePermission):
    def has_permission(self, request, view):
        action = view.action
        if action == 'list':
            return True
        user = request.user
        
        program_id = view.kwargs.get('program_pk')
        try:
            program = Program.objects.get(pk=program_id)
        except Program.DoesNotExist:
            return False
        organization = program.organization
        if action == 'create':
            return (
                organization.created_by == user or
                OrganizationAdmin.objects.filter(
                    user=user,
                    organization=organization,
                    is_active=True
                ).exists() or
                ProgramEventAdmin.objects.filter(
                    user=user,
                    program=program,
                    is_active=True,
                    can_create_events=True
                ).exists()
            )


        # All other actions require authentication
        if not user or not user.is_authenticated:
            return False

        return True

class AttendanceViewSetPermissions(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return True
    def has_object_permission(self, request, view, obj):
        user = request.user
        action = view.action

        if action == 'update_display_name':
            return obj.attendee == user

        if action in ['invalidate_attendance', 'revalidate_attendance']:
            program = obj.event.program
            organization = program.organization
            return (
                organization.created_by == user or
                OrganizationAdmin.objects.filter(
                    user=user,
                    organization=organization,
                    is_active=True,
                    can_change_attendance_validity=True
                ).exists() or
                ProgramEventAdmin.objects.filter(
                    user=user,
                    program=program,
                    is_active=True,
                    can_change_attendance_validity=True
                ).exists()
            )

        return False

class NestedAttendanceViewSetPermissions(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        action = view.action
        if not user or not user.is_authenticated:
            return False
        event_id = view.kwargs.get('event_pk')
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return False
        program = event.program
        organization = program.organization

        if action == 'list':
            return (
                user.is_staff or
                organization.created_by == user or
                OrganizationAdmin.objects.filter(
                    user=user,
                    organization=organization,
                    is_active=True
                ).exists() or
                ProgramEventAdmin.objects.filter(
                    user=user,
                    program=program,
                    is_active=True
                ).exists()
            )

        if action == 'create':
            return user and user.is_authenticated  # Only requires authentication (checked in has_permission)

        return False
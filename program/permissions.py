from rest_framework.permissions import BasePermission
from organization.models import Organization, OrganizationAdmin
from .models import Program, ProgramEventAdmin


class ProgramViewsetPermissions(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        action = view.action

        # Actions that require organization code in request data
        if action == 'create_program':
            org_code = request.data.get('code')
            if not org_code:
                return False  # No organization code provided

            try:
                organization = Organization.objects.get(code=org_code)
            except Organization.DoesNotExist:
                return False

            # Allow if user created the organization
            if organization.created_by == user:
                return True

            # Allow if user is an active org admin with can_create_programs=True
            return OrganizationAdmin.objects.filter(
                user=user,
                organization=organization,
                is_active=True,
                can_create_programs=True
            ).exists()
        if action == 'my_subscribed_programs':
            return user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        action = view.action

        organization = obj.organization

        if not organization:
            return False
        if action == 'invite_organization':
            org_code = request.data.get('code')
            if not org_code:
                return False  # No organization code provided

            # Allow if user created the organization
            if organization.created_by == user:
                return True

            # Allow if user is an active org admin with can_create_programs=True
            return OrganizationAdmin.objects.filter(
                user=user,
                organization=organization,
                is_active=True,
                can_create_programs=True
            ).exists()
            
        # Archive program permissions
        if action == 'archive_program':
            return (
                user.is_staff or
                organization.created_by == user or
                OrganizationAdmin.objects.filter(
                    user=user,
                    organization=organization,
                    is_active=True,
                    can_create_programs=True
                ).exists() or
                ProgramEventAdmin.objects.filter(
                    user=user,
                    program=obj,
                    is_active=True,
                    can_archive_program=True
                ).exists()
            )

        if action in ['assign_program_event_admin', 'revoke_program_event_admin', 'update_program_event_admin']:
            return (
                organization.created_by == user or
                OrganizationAdmin.objects.filter(
                    user=user,
                    organization=organization,
                    is_active=True
                ).exists() or
                ProgramEventAdmin.objects.filter(
                    user=user,
                    program=obj,
                    is_active=True,
                    can_add_another_admin=True
                ).exists()
            )

        if action in ['get_all_program_event_admins', 'get_user_program_event_admins']:
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
                    program=obj,
                    is_active=True
                ).exists()
            )

        if action in ['subscribe', 'unsubscribe']:
            return True

        return False

class ProgramInviteViewsetPermissions(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return True
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        action = view.action
        if action in ['accept_invite', 'reject_invite']:
            # Allow if user is an active org admin for the invited organization
            return (
                obj.organization.created_by == user or
                OrganizationAdmin.objects.filter(
                    user=user,
                    organization=obj.organization,
                    can_create_programs=True,
                    is_active=True
                ).exists()
            )

        if action == 'undo_invite_organization':
            # Allow if user is an active org admin for the inviter organization
            return (
                obj.program.organization.created_by == user or
                OrganizationAdmin.objects.filter(
                    user=user,
                    organization=obj.program.organization,
                    can_create_programs=True,
                    is_active=True
                ).exists()
            )
        return False


class ProgramInvitedOrganizationViewsetPermissions(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return True
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        action = view.action
        # Leave program (ProgramInvitedOrganizationViewset)
        if action == 'leave_program':
            # Allow if user is an active org admin for the organization
            return (
                # obj.organization.created_by == user or
                OrganizationAdmin.objects.filter(
                    user=user,
                    organization=obj.organization,
                    is_active=True
                ).exists()
            )
        return False

class NestedOrganizationInviteViewsetPermissions(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        action = view.action
        organization_id = view.kwargs.get('organization_pk')
        if not organization_id:
            return False  # No organization code provided

        try:
            organization = Organization.objects.get(pk=organization_id)
        except Organization.DoesNotExist:
            return False
        if action == 'list':
            # Allow if user is an active org admin for the invited organization
            return (
                organization.created_by == user or
                OrganizationAdmin.objects.filter(
                    user=user,
                    organization=organization,
                    can_create_programs=True,
                    is_active=True
                ).exists()
            )
        return False

class NestedSubscribersViewsetPermissions(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        action = view.action
        program_id = view.kwargs.get('program_pk')
        print("p id", program_id)
        if not program_id:
            return False  # No program provided

        try:
            program = Program.objects.get(pk=program_id)
        except Program.DoesNotExist:
            return False

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
        return False


class NestedSubscribedProgramsViewsetPermissions(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        action = view.action
        subscriber_id = view.kwargs.get('subscriber_pk')
        if action == 'list':
            return (
                str(user.id) == subscriber_id or 
                user.is_staff
            )

        return False


class NestedProgramInviteViewsetPermissions(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        action = view.action
        program_id = view.kwargs.get('program_pk')
        if not program_id:
            return False  # No program provided

        try:
            program = Program.objects.get(pk=program_id)
        except Program.DoesNotExist:
            return False
        organization = program.organization
        if action == 'list':
            # Allow if user is an active org admin for the invited organization and can create programs
            return (
                organization.created_by == user or
                OrganizationAdmin.objects.filter(
                    user=user,
                    organization=organization,
                    can_create_programs=True,
                    is_active=True
                ).exists()
            )
        return False
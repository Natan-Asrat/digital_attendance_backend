from rest_framework.permissions import BasePermission
from .models import Organization, OrganizationAdmin

class OrganizationPermissions(BasePermission):
    def has_permission(self, request, view):
        # All actions require authentication
        action = view.action
        user = request.user
        
        if action == 'list':
            return True

        # Action requiring superuser or staff with can_add_staff
        if action == 'assign_staff':
            return user and user.is_authenticated and (
                    user.is_superuser or (
                        user.is_staff and user.can_add_staff
                    )
                )

        # Action requiring superuser or staff with can_revoke_staff
        if action == 'revoke_staff':
            return user and user.is_authenticated and (
                    user.is_superuser or (
                        user.is_staff and user.can_revoke_staff
                    )
                )

        # Action requiring superuser or staff
        if action in [
            'assign_organization_super_admin',
            'revoke_organization_super_admin',
            'get_user_organizations'
        ]:
            return user and user.is_authenticated and (
                    user.is_superuser or user.is_staff
                )
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        action = view.action

        # Actions requiring user to be creator or active admin with specific permissions
        if action == 'assign_organization_admin':
            return (
                obj.created_by == user or
                OrganizationAdmin.objects.filter(
                    user=user,
                    organization=obj,
                    is_active=True,
                    can_add_another_admin=True
                ).exists()
            )
        # Actions requiring creator (organizational super admin)
        if action in ['revoke_organization_admin', 'update_organization_admin']:
            return obj.created_by == user

        # Actions requiring staff, creator, or active admin with specific permissions
        if action == 'archive_organization':
            return (
                user.is_staff or
                obj.created_by == user or
                OrganizationAdmin.objects.filter(
                    user=user,
                    organization=obj,
                    is_active=True,
                    can_archive_organization=True
                ).exists()
            )

        # Actions requiring staff, creator, or any active admin
        if action in ['get_all_organizational_admins', 'get_user_organizational_admins']:
            return (
                user.is_staff or
                obj.created_by == user or
                OrganizationAdmin.objects.filter(
                    user=user,
                    organization=obj,
                    is_active=True
                ).exists()
            )

        return False
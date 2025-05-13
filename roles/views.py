from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from organization.models import Organization, OrganizationAdmin
from program.models import ProgramEventAdmin
from organization.serializers import OrganizationAdminSerializer, OrganizationalAdmin_AdminSerializer
from program.serializers import ProgramEventAdmin_AdminSerializer
from account.serializers import UserAdminSerializer
from account.models import User
from .swagger_schema import roles_schema

@roles_schema
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def roles(request):
    organizations_created = Organization.objects.filter(created_by=request.user).select_related('created_by', 'archived_by')
    organizations_serializer = OrganizationAdminSerializer(organizations_created, many=True)
    
    organizational_admin_positions = OrganizationAdmin.objects.filter(user=request.user).select_related('user', 'added_by', 'removed_by', 'organization')
    organizational_admin_serializer = OrganizationalAdmin_AdminSerializer(organizational_admin_positions, many=True)

    program_event_admin_positions = ProgramEventAdmin.objects.filter(user=request.user).select_related('user', 'added_by', 'removed_by', 'program', 'program__organization')
    program_event_admin_serializer = ProgramEventAdmin_AdminSerializer(program_event_admin_positions, many=True)
    user = User.objects.select_related(
        'banned_by',
        'unbanned_by',
        'granted_organizational_permission_by',
        'revoked_organizational_permission_by',
        'granted_staff_status_by',
        'revoked_staff_status_by'
    ).get(id=request.user.id)

    user_serializer = UserAdminSerializer(user)

    data = {
        "user": user_serializer.data,
        "organizations": organizations_serializer.data,
        "organizational_admin_positions": organizational_admin_serializer.data,
        "program_event_admin_positions": program_event_admin_serializer.data
    }
    return Response(data, status=status.HTTP_200_OK)

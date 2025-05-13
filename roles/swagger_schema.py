from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiResponse, OpenApiExample
from rest_framework import serializers
from account.serializers import UserAdminSerializer
from organization.serializers import OrganizationAdminSerializer, OrganizationalAdmin_AdminSerializer
from program.serializers import ProgramEventAdmin_AdminSerializer

roles_schema = extend_schema(
    summary="Get My Roles",
    description=(
        "Returns details about the currently authenticated user's roles:\n\n"
        "- User profile info\n"
        "- Organizations created by the user\n"
        "- Organization admin roles held by the user\n"
        "- Program event admin roles held by the user\n"
    ),
    tags=["26. My Roles"],
    responses={
        200: OpenApiResponse(
            description="Success",
            response= inline_serializer(
                name="RolesResponse",
                fields={
                    "user": UserAdminSerializer(),
                    "organizations": OrganizationAdminSerializer(many=True),
                    "organizational_admin_positions": OrganizationalAdmin_AdminSerializer(many=True),
                    "program_event_admin_positions": ProgramEventAdmin_AdminSerializer(many=True),
                }
            ),
            examples=[
                OpenApiExample(
                    name="Success Example",
                    value={
                        "user": {
                            "id": "b3a20e0f-9b1d-4b1a-9c6d-5f1fbdc402f7",
                            "email": "john@example.com",
                            "phone": "111",
                            "name": "john doe",
                            "is_active": True,
                            "is_superuser": False,
                            "is_staff": False,
                            "date_joined": "2024-01-01T12:00:00Z",
                            "last_seen": None,
                            "banned_by": None,
                            "unbanned_by": None,
                            "banned_at": None,
                            "unbanned_at": None,
                            "can_create_organizations": False,
                            "granted_organizational_permission_by": {
                                "id": "b3a20e0f-9b1d-4b1a-9c6d-5f1fbdc402f7",
                                "email": "john@example.com",
                                "phone": "111",
                                "name": "john doe"
                            },
                            "revoked_organizational_permission_by": None,
                            "granted_organizational_permission_at": None,
                            "revoked_organizational_permission_at": None,
                            "can_add_staff": False,
                            "can_revoke_staff": False,
                            "granted_staff_status_by": None,
                            "revoked_staff_status_by": None,
                            "granted_staff_status_at": None,
                            "revoked_staff_status_at": None,
                        },
                        "organizations": [
                            {
                                "id": 1,
                                "code": "ORG001",
                                "name": "Org Name",
                                "is_active": True,
                                "created_at": "2023-01-01T00:00:00Z",
                                "archived_at": None,
                                "created_by": {
                                    "id": 2,
                                    "email": "admin@example.com",
                                    "phone": "222",
                                    "name": "Admin User"
                                },
                                "archived_by": None
                            }
                        ],
                        "organizational_admin_positions": [
                            {
                                "id": 10,
                                "role": "Organization Manager",
                                "is_active": True,
                                "is_organization_super_admin": False,
                                "can_add_another_admin": False,
                                "can_archive_organization": False,
                                "can_change_attendance_validity": False,
                                "can_create_programs": False,
                                "user": {
                                    "id": 1,
                                    "email": "john@example.com",
                                    "phone": "111",
                                    "name": "john doe"
                                },
                                "organization": {
                                    "id": 1,
                                    "code": "ORG001",
                                    "name": "Org Name",
                                    "is_active": True
                                },
                                "added_by": {
                                    "id": 2,
                                    "email": "admin@example.com",
                                    "phone": "222",
                                    "name": "Admin User"
                                },
                                "removed_by": None,
                            }
                        ],
                        "program_event_admin_positions": [
                            {
                                "id": 20,
                                "role": "Program Creator",
                                "is_active": True,
                                "is_program_super_admin": False,
                                "can_add_another_admin": False,
                                "can_archive_program": False,
                                "can_archive_event": False,
                                "can_add_event_organizer": False,
                                "can_remove_event_organizer_from_program": False,
                                "can_change_attendance_validity": False,
                                "can_create_events": False,
                                "can_conclude_events": False,
                                "user": {
                                    "id": 1,
                                    "email": "john@example.com",
                                    "phone": "111",
                                    "name": "john doe"
                                },
                                "program": {
                                    "id": 1,
                                    "name": "Program 1",
                                    "organization": {
                                        "id": 1,
                                        "code": "ORG001",
                                        "name": "Org Name",
                                        "is_active": True
                                    },
                                    "is_active": True,
                                    "created_at": "2023-01-01T00:00:00Z"
                                },
                                "added_by": {
                                    "id": 2,
                                    "email": "admin@example.com",
                                    "phone": "222",
                                    "name": "Admin User"
                                },
                                "removed_by": None,
                                "added_at": "2023-01-01T00:00:00Z",
                                "removed_at": None,
                                "left_at": None
                            }
                        ]
                    },
                    response_only=True
                )
            ]
        ),
    }

)

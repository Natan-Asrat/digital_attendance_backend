from drf_spectacular.utils import OpenApiResponse, OpenApiExample, inline_serializer, extend_schema
from rest_framework import serializers

# 2
assign_staff_schema = extend_schema(
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'email': {
                    'type': 'string',
                    'format': 'email',
                    'description': 'Email of the user to assign as staff.'
                }
            },
            'required': ['email'],
        }
    },
    responses={
        200: OpenApiResponse(
            description="Success",
            response=inline_serializer(
                name="AssignStaffSuccess",
                fields={
                    "message": serializers.CharField(
                        help_text="User assigned as Staff successfully."
                    )
                }
            ),
            examples=[
                OpenApiExample(
                    name="Success Example",
                    value={"message": "User assigned as Staff successfully."},
                    response_only=True
                )
            ]
        ),
        400: OpenApiResponse(
            description="Bad Request",
            response=inline_serializer(
                name="AssignStaffBadRequest",
                fields={
                    "error": serializers.CharField()
                }
            ),
            examples=[
                OpenApiExample(
                    name="Error - User is banned",
                    description="User is banned",
                    value={"error": "User is banned."},
                    response_only=True
                ),
                OpenApiExample(
                    name="Error - User revoked permissions",
                    description="User has been revoked from Staff permission",
                    value={"error": "User has been revoked Staff permission."},
                    response_only=True
                ),
                OpenApiExample(
                    name="Error - User already has permission",
                    description="User has already been granted permission",
                    value={"error": "User has already been granted Staff permission."},
                    response_only=True
                )
            ]
        ),
        403: OpenApiResponse(
            description="Trying to change a superuser account: Forbidden.",
            response=inline_serializer(
                name="AssignStaffForbidden",
                fields={
                    "detail": serializers.CharField()
                }
            ),
            examples=[OpenApiExample(
                name="Error - Forbidden",
                value={"detail": "You are not allowed to alter this account"},
                response_only=True
            )]
        ),
        404: OpenApiResponse(
            description="Not Found",
            response=inline_serializer(
                name="AssignStaffNotFound",
                fields={
                    "detail": serializers.CharField()
                }
            ),
            examples=[
                OpenApiExample(
                    name="Error - User not found",
                    description="User not found",
                    value={"detail": "User not found."},
                    response_only=True
                )
            ]
        )
    },
    description="Assign a user as Staff if the user is active, hasn't been revoked permission, and hasn't already been granted permission.",
    summary="Assign Staff",
    tags=["2. Assign/Revoke Staff (by Staff)"]
)

revoke_staff_schema = extend_schema(
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'email': {
                    'type': 'string',
                    'format': 'email',
                    'description': 'Email of the user to revoke Staff permissions from.'
                }
            },
            'required': ['email'],
        }
    },
    responses={
        200: OpenApiResponse(
            description="Success",
            response=inline_serializer(
                name="RevokeStaffSuccess",
                fields={
                    "message": serializers.CharField(
                        help_text="User has been revoked Staff permissions successfully."
                    )
                }
            ),
            examples=[
                OpenApiExample(
                    name="Success Example",
                    value={"message": "User has been revoked Staff permissions successfully."},
                    response_only=True
                )
            ]
        ),
        400: OpenApiResponse(
            description="Bad Request",
            response=inline_serializer(
                name="RevokeStaffBadRequest",
                fields={
                    "error": serializers.CharField()
                }
            ),
            examples=[
                OpenApiExample(
                    name="Error - User is banned",
                    description="User is banned",
                    value={"error": "User is banned."},
                    response_only=True
                ),
                OpenApiExample(
                    name="Error - User already revoked",
                    description="User has already been revoked Staff permissions.",
                    value={"error": "User has already been revoked Staff permissions."},
                    response_only=True
                )
            ]
        ),
        403: OpenApiResponse(
            description="Trying to change a superuser account: Forbidden.",
            response=inline_serializer(
                name="RevokeStaffForbidden",
                fields={
                    "detail": serializers.CharField()
                }
            ),
            examples=[OpenApiExample(
                name="Error - Forbidden",
                value={"detail": "You are not allowed to alter this account"},
                response_only=True
            )]
        ),
        404: OpenApiResponse(
            description="Not Found",
            response=inline_serializer(
                name="RevokeStaffNotFound",
                fields={
                    "detail": serializers.CharField()
                }
            ),
            examples=[
                OpenApiExample(
                    name="Error - User not found",
                    description="User not found",
                    value={"detail": "User not found."},
                    response_only=True
                )
            ]
        )
    },
    description="Revoke a user's Staff permission if they are active and haven't already been revoked.",
    summary="Revoke Staff",
    tags=["2. Assign/Revoke Staff (by Staff)"]
)

# 3
assign_organization_super_admin_schema = extend_schema(
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'email': {
                    'type': 'string',
                    'format': 'email',
                    'description': 'Email of the user to assign as organization super admin.'
                }
            },
            'required': ['email'],
        }
    },
    responses={
        200: OpenApiResponse(
            description="Success",
            response=inline_serializer(
                name="AssignOrganizationSuperAdminSuccess",
                fields={
                    "message": serializers.CharField(
                        help_text="User assigned as organizational super admin successfully."
                    )
                }
            ),
            examples=[
                OpenApiExample(
                    name="Success Example",
                    value={"message": "User assigned as organizational super admin successfully."},
                    response_only=True
                )
            ]
        ),
        400: OpenApiResponse(
            description="Bad Request",
            response=inline_serializer(
                name="AssignOrganizationSuperAdminBadRequest",
                fields={
                    "error": serializers.CharField()
                }
            ),
            examples=[
                OpenApiExample(
                    name="Error - User is banned",
                    description="User is banned",
                    value={"error": "User is banned."},
                    response_only=True
                ),
                OpenApiExample(
                    name="Error - User revoked permissions",
                    description="User has revoked organizational permission",
                    value={"error": "User has been revoked organizational super admin permission."},
                    response_only=True
                ),
                OpenApiExample(
                    name="Error - User already has permission",
                    description="User has already been granted permission",
                    value={"error": "User has already been granted organizational super admin permission."},
                    response_only=True
                )
            ]
        ),
        400: OpenApiResponse(
            description="Bad Request",
            response=inline_serializer(
                name="AssignOrganizationSuperAdminBadRequest",
                fields={
                    "error": serializers.CharField()
                }
            ),
            examples=[
                OpenApiExample(
                    name="Error - User is banned",
                    description="User is banned",
                    value={"error": "User is banned."},
                    response_only=True
                ),
                OpenApiExample(
                    name="Error - User revoked permissions",
                    description="User has revoked organizational permission",
                    value={"error": "User has been revoked organizational super admin permission."},
                    response_only=True
                ),
                OpenApiExample(
                    name="Error - User already has permission",
                    description="User has already been granted permission",
                    value={"error": "User has already been granted organizational super admin permission."},
                    response_only=True
                )
            ]
        ),
        404: OpenApiResponse(
            description="Not Found",
            response=inline_serializer(
                name="AssignOrganizationSuperAdminNotFound",
                fields={
                    "detail": serializers.CharField()
                }
            ),
            examples=[
                OpenApiExample(
                    name="Error - User not found",
                    description="User not found",
                    value={"detail": "User not found."},
                    response_only=True
                )
            ]
        )
    },
    description="Assign a user as an organizational super admin if the user is active, hasn't been revoked permission, and hasn't already been granted permission.",
    summary="Assign Organization Super Admin",
    tags=["3. Assign/Revoke Organizational Super Admin (by Staff)"]
)

revoke_organization_super_admin_schema = extend_schema(
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'email': {
                    'type': 'string',
                    'format': 'email',
                    'description': 'Email of the user to revoke organization super admin permissions from.'
                }
            },
            'required': ['email'],
        }
    },
    responses={
        200: OpenApiResponse(
            description="Success",
            response=inline_serializer(
                name="RevokeOrganizationSuperAdminSuccess",
                fields={
                    "message": serializers.CharField(
                        help_text="User has been revoked organizational super admin permission successfully."
                    )
                }
            ),
            examples=[
                OpenApiExample(
                    name="Success Example",
                    value={"message": "User has been revoked organizational super admin permission successfully."},
                    response_only=True
                )
            ]
        ),
        400: OpenApiResponse(
            description="Bad Request",
            response=inline_serializer(
                name="RevokeOrganizationSuperAdminBadRequest",
                fields={
                    "error": serializers.CharField()
                }
            ),
            examples=[
                OpenApiExample(
                    name="Error - User is banned",
                    description="User is banned",
                    value={"error": "User is banned."},
                    response_only=True
                ),
                OpenApiExample(
                    name="Error - User already revoked",
                    description="User has already been revoked organizational super admin permission.",
                    value={"error": "User has already been revoked organizational super admin permission."},
                    response_only=True
                )
            ]
        ),
        404: OpenApiResponse(
            description="Not Found",
            response=inline_serializer(
                name="RevokeOrganizationSuperAdminNotFound",
                fields={
                    "detail": serializers.CharField()
                }
            ),
            examples=[
                OpenApiExample(
                    name="Error - User not found",
                    description="User not found",
                    value={"detail": "User not found."},
                    response_only=True
                )
            ]
        )
    },
    description="Revoke a user's organizational super admin permission if they are active and haven't already been revoked.",
    summary="Revoke Organization Super Admin",
    tags=["3. Assign/Revoke Organizational Super Admin (by Staff)"]
)

# 4
create_organization_schema = extend_schema(
    request=inline_serializer(
        name="CreateOrganizationRequest",
        fields={
            "name": serializers.CharField(help_text="Name of the organization."),
            "code": serializers.CharField(help_text="Unique code for the organization.")
        }
    ),
    responses={
        201: OpenApiResponse(
            description="Organization created successfully.",
            response=inline_serializer(
                name="CreateOrganizationSuccess",
                fields={
                    "id": serializers.UUIDField(help_text="ID of the newly created organization."),
                    "name": serializers.CharField(help_text="Name of the organization."),
                    "code": serializers.CharField(help_text="Unique code for the organization."),
                    "is_archived": serializers.BooleanField(help_text="Whether the organization is active and not archived."),
                }
            ),
            examples=[
                OpenApiExample(
                    name="Success Example",
                    value={
                        "id": "a3f1e59e-2c42-4a62-b08f-5f1bde8655d7",
                        "name": "New Org",
                        "code": "ORG123",
                        "is_archived": True
                    },
                    response_only=True
                )
            ]
        ),
        400: OpenApiResponse(
            description="Bad Request",
            response=inline_serializer(
                name="CreateOrganizationBadRequest",
                fields={
                    "error": serializers.CharField()
                }
            ),
            examples=[
                OpenApiExample(
                    name="Error - Code already exists",
                    description="Organization code must be unique.",
                    value={
                        "code": [
                            "organization with this code already exists."
                        ]
                    },
                    response_only=True
                )
            ]
        )
    },
    summary="Create Organization",
    description="Creates a new organization with a unique code and name.",
    tags=["4. Create/View Organization (by Organizational Super Admin)"]
)

view_all_organizations_schema = extend_schema(
    responses=inline_serializer(
        name="ViewAllOrganizationsCreated",
        fields={
            "count": serializers.IntegerField(),
            "next": serializers.CharField(allow_null=True),
            "previous": serializers.CharField(allow_null=True),
            "results": serializers.ListField(
                child=inline_serializer(
                    name="OrganizationAdminItem",
                    fields={
                        "id": serializers.UUIDField(),
                        "code": serializers.CharField(),
                        "name": serializers.CharField(),
                        "is_active": serializers.BooleanField(),
                        "created_at": serializers.DateTimeField(),
                        "archived_at": serializers.DateTimeField(allow_null=True),
                        "created_by": serializers.UUIDField(),
                        "archived_by": serializers.UUIDField(allow_null=True),
                    }
                )
            )
        }
    ),
    summary="View All Organizations Created",
    description="Retrieves a paginated list of all organizations created by the current user.",
    tags=["4. Create/View Organization (by Organizational Super Admin)"],
)

view_active_organizations_schema = extend_schema(
    responses=inline_serializer(
        name="ViewActiveOrganizationsCreated",
        fields={
            "count": serializers.IntegerField(),
            "next": serializers.CharField(allow_null=True),
            "previous": serializers.CharField(allow_null=True),
            "results": serializers.ListField(
                child=inline_serializer(
                    name="OrganizationAdminItem",
                    fields={
                        "id": serializers.UUIDField(),
                        "code": serializers.CharField(),
                        "name": serializers.CharField(),
                        "is_active": serializers.BooleanField(),
                        "created_at": serializers.DateTimeField(),
                        "archived_at": serializers.DateTimeField(allow_null=True),
                        "created_by": serializers.UUIDField(),
                        "archived_by": serializers.UUIDField(allow_null=True),
                    }
                )
            )
        }
    ),
    summary="View Active Organizations Created",
    description="Retrieves a paginated list of active organizations created by the current user.",
    tags=["4. Create/View Organization (by Organizational Super Admin)"],
)

view_archived_organizations_schema = extend_schema(
    responses=inline_serializer(
        name="ViewArchivedOrganizationsCreated",
        fields={
            "count": serializers.IntegerField(),
            "next": serializers.CharField(allow_null=True),
            "previous": serializers.CharField(allow_null=True),
            "results": serializers.ListField(
                child=inline_serializer(
                    name="OrganizationAdminItem",
                    fields={
                        "id": serializers.UUIDField(),
                        "code": serializers.CharField(),
                        "name": serializers.CharField(),
                        "is_active": serializers.BooleanField(),
                        "created_at": serializers.DateTimeField(),
                        "archived_at": serializers.DateTimeField(allow_null=True),
                        "created_by": serializers.UUIDField(),
                        "archived_by": serializers.UUIDField(allow_null=True),
                    }
                )
            )
        }
    ),
    summary="View Archived Organizations Created",
    description="Retrieves a paginated list of archived organizations created by the current user.",
    tags=["4. Create/View Organization (by Organizational Super Admin)"],
)

# 5
archive_organization_schema = extend_schema(
    summary="Archive an Organization",
    description=(
        "Archives the specified organization by marking it as inactive, setting the archive timestamp, "
        "and recording the staff user who performed the action.\n\n"
        "**Only staff users are authorized to archive organizations.**\n\n"
        "Returns:\n"
        "- 200 on successful archive\n"
        "- 400 if already archived\n"
        "- 403 if the user is not staff\n"
        "- 404 if the organization does not exist"
    ),
    tags=["5. Archive Organization (by Staff)"],
    request=None,  
    responses={
        200: inline_serializer(
            name="ArchivedOrganizationResponse",
            fields={
                "id": serializers.UUIDField(),
                "code": serializers.CharField(),
                "name": serializers.CharField(),
                "is_active": serializers.BooleanField(default=False),
                "created_at": serializers.DateTimeField(),
                "archived_at": serializers.DateTimeField(allow_null=True),
                "created_by": serializers.UUIDField(),
                "archived_by": serializers.UUIDField(allow_null=True),
            }
        ),
        400: OpenApiResponse(
            description="Bad Request - if already archived",
            response=inline_serializer(
                name="ArchiveOrganization400",
                fields={"error": serializers.CharField()},
            ),
            examples=[
                OpenApiExample(
                    name="Already Archived",
                    description="Organization is already archived and cannot be archived again.",
                    value={"error": "Organization is already archived."},
                    response_only=True,
                    status_codes=["400"]
                )
            ]
        ),
        403: inline_serializer(
            name="ArchiveOrganization403",
            fields={"detail": serializers.CharField(default="You do not have permission to perform this action.")}
        ),
        404: inline_serializer(
            name="ArchiveOrganization404",
            fields={"detail": serializers.CharField(default="No Organization matches the given query.")}
        ),
    }
)
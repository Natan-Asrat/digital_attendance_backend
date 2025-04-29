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
                    "error": serializers.CharField()
                }
            ),
            examples=[OpenApiExample(
                name="Error - Forbidden",
                value={"error": "You are not allowed to alter this account"},
                response_only=True
            )]
        ),
        404: OpenApiResponse(
            description="Not Found",
            response=inline_serializer(
                name="AssignStaffNotFound",
                fields={
                    "error": serializers.CharField()
                }
            ),
            examples=[
                OpenApiExample(
                    name="Error - User not found",
                    description="User not found",
                    value={"error": "User not found."},
                    response_only=True
                )
            ]
        )
    },
    description="Assign a user as Staff if the user is active, hasn't been revoked permission, and hasn't already been granted permission.",
    summary="Assign Staff",
    tags=["2. Assign/Revoke Staff"]
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
                    "error": serializers.CharField()
                }
            ),
            examples=[OpenApiExample(
                name="Error - Forbidden",
                value={"error": "You are not allowed to alter this account"},
                response_only=True
            )]
        ),
        404: OpenApiResponse(
            description="Not Found",
            response=inline_serializer(
                name="RevokeStaffNotFound",
                fields={
                    "error": serializers.CharField()
                }
            ),
            examples=[
                OpenApiExample(
                    name="Error - User not found",
                    description="User not found",
                    value={"error": "User not found."},
                    response_only=True
                )
            ]
        )
    },
    description="Revoke a user's Staff permission if they are active and haven't already been revoked.",
    summary="Revoke Staff",
    tags=["2. Assign/Revoke Staff"]
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
                    "error": serializers.CharField()
                }
            ),
            examples=[
                OpenApiExample(
                    name="Error - User not found",
                    description="User not found",
                    value={"error": "User not found."},
                    response_only=True
                )
            ]
        )
    },
    description="Assign a user as an organizational super admin if the user is active, hasn't been revoked permission, and hasn't already been granted permission.",
    summary="Assign Organization Super Admin",
    tags=["3. Assign/Revoke Organizational Super Admin"]
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
                    "error": serializers.CharField()
                }
            ),
            examples=[
                OpenApiExample(
                    name="Error - User not found",
                    description="User not found",
                    value={"error": "User not found."},
                    response_only=True
                )
            ]
        )
    },
    description="Revoke a user's organizational super admin permission if they are active and haven't already been revoked.",
    summary="Revoke Organization Super Admin",
    tags=["3. Assign/Revoke Organizational Super Admin"]
)
from drf_spectacular.utils import OpenApiResponse, OpenApiExample, OpenApiParameter, inline_serializer, extend_schema
from .serializers import (
    ProgramAdminSerializer, 
    ProgramSerializer, 
    InvitedOrganizationProgramAdminSerializer,
    ProgramInviteSerializer,
    InvitedOrganizationProgramSerializer
)

from rest_framework import serializers

# 9

create_program_schema = extend_schema(
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'name': {
                    'type': 'string',
                    'description': 'Name of the program.'
                },
                'code': {
                    'type': 'string',
                    'description': 'Code of the organization.'
                }
            },
            'required': ['name', 'code']
        }
    },
    
    responses={
        200: ProgramAdminSerializer,
        400: OpenApiResponse(
            description="Bad Request",
            response=inline_serializer(
                name="CreateProgramBadRequest",
                fields={
                    "error": serializers.CharField()
                }
            ),
            examples=[
                OpenApiExample(
                    name="Error - Organization is banned",
                    description="Organization is banned",
                    value={"error": "Organization is banned."},
                    response_only=True
                )
            ]
        ),
        403: OpenApiResponse(
            description="Trying to change a superuser account: Forbidden.",
            response=inline_serializer(
                name="CreateProgramForbidden",
                fields={
                    "detail": serializers.CharField()
                }
            ),
            examples=[OpenApiExample(
                name="Error - Forbidden",
                value={"detail": "You do not have permission to perform this action."},
                response_only=True
            )]
        ),
        404: OpenApiResponse(
            description="Not Found",
            response=inline_serializer(
                name="CreateProgramNotFound",
                fields={
                    "detail": serializers.CharField()
                }
            ),
            examples=[
                OpenApiExample(
                    name="Error - Organization not found",
                    description="Organization not found",
                    value={"detail": "Organization not found."},
                    response_only=True
                )
            ]
        )
    },
    description="Create a program for the organization with the given code.",
    summary="Create Program",
    tags=["9. Create/View/Archive Program (by Organizational Super Admin & Organizational Admin)"]
)

archive_program_schema = extend_schema(
    summary="Archive a Program",
    description=(
        "Archives the specified program by marking it as inactive, setting the archive timestamp, "
        "and recording the user who performed the action.\n\n"
    ),
    tags=["9. Create/View/Archive Program (by Organizational Super Admin & Organizational Admin)"],
    request=None,  
    responses={
        200: ProgramSerializer,
        400: OpenApiResponse(
            description="Bad Request - if already archived",
            response=inline_serializer(
                name="ArchiveProgram400",
                fields={"error": serializers.CharField()},
            ),
            examples=[
                OpenApiExample(
                    name="Already Archived",
                    description="Program is already archived and cannot be archived again.",
                    value={"error": "Program is already archived."},
                    response_only=True,
                    status_codes=["400"]
                )
            ]
        ),
        403: inline_serializer(
            name="ArchiveProgram403",
            fields={"detail": serializers.CharField(default="You do not have permission to perform this action.")}
        ),
        404: inline_serializer(
            name="ArchiveProgram404",
            fields={"detail": serializers.CharField(default="No Program matches the given query.")}
        ),
    }
)

list_organization_programs_schema = extend_schema(
    summary="List Organization Programs",
    description=(
        "Lists all programs created by the specified organization.\n\n"
    ),
    tags=["9. Create/View/Archive Program (by Organizational Super Admin & Organizational Admin)"],
    responses={
        200: ProgramAdminSerializer(many=True),
        404: inline_serializer(
            name="ListOrganizationPrograms404",
            fields={"detail": serializers.CharField(default="No Organization matches the given query.")}
        ),
    }
)

list_organization_associated_programs_schema = extend_schema(
    summary="List Associated Programs",
    description=(
        "Lists all programs associated with the specified organization.\n\n"
    ),
    tags=["9. Create/View/Archive Program (by Organizational Super Admin & Organizational Admin)"],
    responses={
        200: ProgramAdminSerializer(many=True),
        404: inline_serializer(
            name="ListOrganizationPrograms404",
            fields={"detail": serializers.CharField(default="No Organization matches the given query.")}
        ),
    }
)

# 10

invite_organization_schema = extend_schema(
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'code': {
                    'type': 'string',
                    'description': 'Code of the organization to invite.'
                }
            },
            'required': ['code']
        }
    },
    summary="Invite Organizations to Program",
    description=(
        "Invites an organization to join the specified program.\n\n"
    ),
    tags=["10. Invite/Undo Invite (by Organizational Super Admin & Organizational Admin)"],
    

)


undo_invite_organization_schema = extend_schema(
    summary="Undo Organization Invite",
    description="Marks the invite as undone (inactive). Also updates the related `InvitedOrganizationProgram` if it exists.",
    tags=["10. Invite/Undo Invite (by Organizational Super Admin & Organizational Admin)"],
    request=None,
    responses={
        200: ProgramInviteSerializer,
        400: OpenApiResponse(
            description="Bad Request",
            response=inline_serializer(
                name="UndoInviteBadRequest",
                fields={"error": serializers.CharField()}
            ),
            examples=[
                OpenApiExample(
                    name="Already Undone",
                    value={"error": "Invite is already undone."},
                    response_only=True,
                    status_codes=["400"]
                ),
                OpenApiExample(
                    name="Already Removed",
                    value={"error": "Invite is already removed."},
                    response_only=True,
                    status_codes=["400"]
                )
            ]
        )
    }
)

# 11
accept_invite_schema = extend_schema(
    summary="Accept Invite",
    description="Accepts the organization invite and creates an active `InvitedOrganizationProgram` instance.",
    tags=["11. Accept/Reject/Leave/View Invite (by other Organizational Super Admin & other Organizational Admin)"],
    request=None,
    responses={
        200: ProgramInviteSerializer,
        400: OpenApiResponse(
            description="Bad Request",
            response=inline_serializer(
                name="AcceptInviteBadRequest",
                fields={"error": serializers.CharField()}
            ),
            examples=[
                OpenApiExample(
                    name="Already Accepted",
                    value={"error": "Invite is already accepted."},
                    response_only=True
                ),
                OpenApiExample(
                    name="Undone Invite",
                    value={"error": "Invite is undone."},
                    response_only=True
                ),
                OpenApiExample(
                    name="Already in Program",
                    value={"error": "Organization is already in this program."},
                    response_only=True
                )
            ]
        )
    }
)

reject_invite_schema = extend_schema(
    summary="Reject Invite",
    description="Rejects the organization invite and updates `InvitedOrganizationProgram` if it exists.",
    tags=["11. Accept/Reject/Leave/View Invite (by other Organizational Super Admin & other Organizational Admin)"],
    request=None,
    responses={
        200: ProgramInviteSerializer,
        400: OpenApiResponse(
            description="Bad Request",
            response=inline_serializer(
                name="RejectInviteBadRequest",
                fields={"error": serializers.CharField()}
            ),
            examples=[
                OpenApiExample(
                    name="Already Rejected",
                    value={"error": "Invite is already rejected."},
                    response_only=True
                ),
                OpenApiExample(
                    name="Undone Invite",
                    value={"error": "Invite is undone."},
                    response_only=True
                )
            ]
        )
    }
)

list_program_invites_schema = extend_schema(
    summary="List Invites sent in a specific Program",
    description=(
        "Lists all invites sent by a program to organizations.\n\n"
    ),
    tags=["11. Accept/Reject/Leave/View Invite (by other Organizational Super Admin & other Organizational Admin)"],
    responses={
        200: ProgramInviteSerializer(many=True),
        404: inline_serializer(
            name="ListProgramInvites404",
            fields={"detail": serializers.CharField(default="No Program matches the given query.")}
        ),
    }
)

list_organizations_invites_schema = extend_schema(
    summary="List Invites to join programs sent to a specific Organization",
    description=(
        "Lists all invites sent to join programs to a specific organization.\n\n"
    ),
    tags=["11. Accept/Reject/Leave/View Invite (by other Organizational Super Admin & other Organizational Admin)"],
    responses={
        200: ProgramInviteSerializer(many=True),
        404: inline_serializer(
            name="ListProgramInvites404",
            fields={"detail": serializers.CharField(default="No Organization matches the given query.")}
        ),
    }
)

leave_program_schema = extend_schema(
    summary="Leave Program",
    description="Leaves the specified program.",
    tags=["11. Accept/Reject/Leave/View Invite (by other Organizational Super Admin & other Organizational Admin)"],
    request=None,
    responses={
        200: InvitedOrganizationProgramSerializer,
        400: OpenApiResponse(
            description="Bad Request",
            response=inline_serializer(
                name="LeaveProgramBadRequest",
                fields={"error": serializers.CharField()}
            ),
            examples=[
                OpenApiExample(
                    name="Already Left",
                    value={"error": "Had left the program already."},
                    response_only=True
                ),
                OpenApiExample(
                    name="Already Undone",
                    value={"error": "Invite is already undone."},
                    response_only=True,
                    status_codes=["400"]
                ),
            ]
        )
    }
)

list_organization_invited_programs_schema = extend_schema(
    summary="List Invited Programs",
    description=(
        "Lists all programs invited and accepted to the specified organization. (Has more detail than /programs/associated_programs/ with details on who accepted, rejected, removed invite... for administrative purposes)\n\n"
    ),
    tags=["11. Accept/Reject/Leave/View Invite (by other Organizational Super Admin & other Organizational Admin)"],
    responses={
        200: InvitedOrganizationProgramAdminSerializer(many=True),
        404: inline_serializer(
            name="ListOrganizationPrograms404",
            fields={"detail": serializers.CharField(default="No Organization matches the given query.")}
        ),
    }
)


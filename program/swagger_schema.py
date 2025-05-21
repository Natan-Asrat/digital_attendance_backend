from drf_spectacular.utils import OpenApiResponse, OpenApiExample, OpenApiParameter, inline_serializer, extend_schema
from .serializers import (
    ProgramAdminSerializer, 
    ProgramSerializer, 
    InvitedOrganizationProgramAdminSerializer,
    ProgramInviteSerializer,
    InvitedOrganizationProgramSerializer,
    ProgramSubscriberGetSubsSerializer,
    ProgramSubscriberGetProgsSerializer,
    ProgramEventAdmin_AdminSerializer,
    AssignProgramEventAdminSerializer,
    PatchProgramEventAdminSerializer
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
            name="ListOrganizationAssociatedPrograms404",
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
    tags=["11. Accept/Reject/View Invite (by other Organizational Super Admin & other Organizational Admin)"],
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
    tags=["11. Accept/Reject/View Invite (by other Organizational Super Admin & other Organizational Admin)"],
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
    tags=["11. Accept/Reject/View Invite (by other Organizational Super Admin & other Organizational Admin)"],
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
    tags=["11. Accept/Reject/View Invite (by other Organizational Super Admin & other Organizational Admin)"],
    responses={
        200: ProgramInviteSerializer(many=True),
        404: inline_serializer(
            name="ListOrgInvites404",
            fields={"detail": serializers.CharField(default="No Organization matches the given query.")}
        ),
    }
)

# 12

leave_program_schema = extend_schema(
    summary="Leave Program",
    description="Leaves the specified program.",
    tags=["12. View/Leave Associated Programs (by other Organizational Super Admin & other Organizational Admin)"],
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
    tags=["12. View/Leave Associated Programs (by other Organizational Super Admin & other Organizational Admin)"],
    responses={
        200: InvitedOrganizationProgramAdminSerializer(many=True),
        404: inline_serializer(
            name="ListOrganizationInvited404",
            fields={"detail": serializers.CharField(default="No Organization matches the given query.")}
        ),
    }
)

# 13

subscribe_program_schema = extend_schema(
    summary="Subscribe to Program",
    description="Subscribes the authenticated user to the specified program. If a previous subscription existed but was inactive, it will be reactivated.",
    tags=["13. Subscribe/Unsubscribe/View to Program (by User)"],
    request=None,
    responses={
        201: OpenApiResponse(
            description="Successfully subscribed to the program.",
            response=inline_serializer(
                name="ProgramSubscriptionSuccess",
                fields={"message": serializers.CharField()}
            ),
            examples=[
                OpenApiExample(
                    name="New Subscription",
                    value={"message": "Successfully subscribed to the program."},
                    response_only=True,
                    status_codes=["201"]
                )
            ]
        ),
        200: OpenApiResponse(
            description="Subscription reactivated successfully.",
            response=inline_serializer(
                name="ProgramSubscriptionReactivated",
                fields={"message": serializers.CharField()}
            ),
            examples=[
                OpenApiExample(
                    name="Reactivated Subscription",
                    value={"message": "Subscription reactivated successfully."},
                    response_only=True,
                    status_codes=["200"]
                )
            ]
        ),
        400: OpenApiResponse(
            description="Bad Request",
            response=inline_serializer(
                name="ProgramSubscriptionBadRequest",
                fields={"error": serializers.CharField()}
            ),
            examples=[
                OpenApiExample(
                    name="Already Subscribed",
                    value={"error": "Already subscribed to this program."},
                    response_only=True,
                    status_codes=["400"]
                ),
                OpenApiExample(
                    name="Archived Program",
                    value={"error": "Program is already archived."},
                    response_only=True,
                    status_codes=["400"]
                ),
            ]
        )
    }
)

unsubscribe_program_schema = extend_schema(
    summary="Unsubscribe from Program",
    description="Unsubscribes the authenticated user from the specified program if currently subscribed.",
    tags=["13. Subscribe/Unsubscribe/View to Program (by User)"],
    request=None,
    responses={
        200: OpenApiResponse(
            description="Successfully unsubscribed from the program.",
            response=inline_serializer(
                name="ProgramUnsubscribeSuccess",
                fields={"message": serializers.CharField()}
            ),
            examples=[
                OpenApiExample(
                    name="Successful Unsubscribe",
                    value={"message": "Successfully unsubscribed from the program."},
                    response_only=True,
                    status_codes=["200"]
                )
            ]
        ),
        400: OpenApiResponse(
            description="Bad Request",
            response=inline_serializer(
                name="ProgramUnsubscribeBadRequest",
                fields={"error": serializers.CharField()}
            ),
            examples=[
                OpenApiExample(
                    name="Not Subscribed",
                    value={"error": "You are not subscribed to this program or have unsubscribed."},
                    response_only=True,
                    status_codes=["400"]
                ),
                OpenApiExample(
                    name="Archived Program",
                    value={"error": "Program is archived."},
                    response_only=True,
                    status_codes=["400"]
                )
            ]
        )
    }
)

my_subscribed_programs_schema = extend_schema(
    summary="My Subscribed Programs",
    description="Returns a list of programs the authenticated user is currently subscribed to.",
    tags=["13. Subscribe/Unsubscribe/View to Program (by User)"],
    request=None,
    responses={
        200: OpenApiResponse(
            description="List of subscribed programs.",
            response=ProgramSubscriberGetProgsSerializer(many=True)
        )
    }
)

# 14

list_subscribers_in_program_schema = extend_schema(
    summary="List Subscribers of a Program",
    description="Returns a paginated list of active subscribers for the specified program.",
    tags=["14. Subscribers in Program (by O. S. Admins, O. Admins, Event Admins & Event Organizers with permission)"],
    responses={
        200: OpenApiResponse(
            description="List of active subscribers.",
            response=ProgramSubscriberGetSubsSerializer(many=True)
        )
    }
)

# 15

list_subscribed_programs_schema = extend_schema(
    summary="List Subscribed Programs of a User",
    description="Returns a paginated list of active programs a specific user has subscribed to.",
    tags=["15. Subscribed Programs of a User (by Staff)"],
    responses={
        200: OpenApiResponse(
            description="List of active subscribed programs.",
            response=ProgramSubscriberGetProgsSerializer(many=True)
        )
    }
)


# 16 
assign_program_event_admin_schema = extend_schema(
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "email": {
                    'type': 'string',
                    'format': 'email',
                    'description': 'Email of the user to assign as program event admin.'
                },
                "role": {
                    'type': 'string',
                    'description': 'Role of the user (Optional - default: Admin).'
                },
                "can_add_another_admin": {
                    'type': 'boolean',
                    'description': 'Can add another admin (Optional - default: False).'
                },
                "can_archive_program": {
                    'type': 'boolean',
                    'description': 'Can archive program (Optional - default: False).'
                },
                "can_archive_event": {
                    'type': 'boolean',
                    'description': 'Can archive event (Optional - default: False).'
                },
                "can_add_event_organizer": {
                    'type': 'boolean',
                    'description': 'Can add event organizer (Optional - default: False).'
                },
                "can_remove_event_organizer_from_program": {
                    'type': 'boolean',
                    'description': 'Can remove event organizer from program (Optional - default: False).'
                },
                "can_change_attendance_validity": {
                    'type': 'boolean',
                    'description': 'Can change attendance validity (Optional - default: False).'
                },
                "can_create_events": {
                    'type': 'boolean',
                    'description': 'Can create events (Optional - default: False).'
                },
                "can_conclude_events": {
                    'type': 'boolean',
                    'description': 'Can conclude events (Optional - default: False).'
                }
            },
            "required": ['email']
        }
    },
    responses={
        200: OpenApiResponse(
            description="Success",
            response=ProgramEventAdmin_AdminSerializer,
        ),
        400: OpenApiResponse(
            description="Bad Request",
            response=inline_serializer(
                name="AssignProgramEventAdminBadRequest",
                fields={
                    "error": serializers.CharField()
                }
            ),
            examples=[
                OpenApiExample(
                    name="Error - Program archived",
                    description="The program is archived.",
                    value={"error": "Program is archived."},
                    response_only=True
                ),
                OpenApiExample(
                    name="Error - User is banned",
                    description="The user is banned and cannot be assigned.",
                    value={"error": "User is banned."},
                    response_only=True
                ),
                OpenApiExample(
                    name="Error - Revoked",
                    description="The user has been revoked as program admin.",
                    value={"error": "User has been revoked as program admin."},
                    response_only=True
                ),
                OpenApiExample(
                    name="Error - Already assigned",
                    description="The user is already an active program admin.",
                    value={"error": "User is already assigned as program admin."},
                    response_only=True
                ),
            ]
        ),
        404: OpenApiResponse(
            description="Not Found",
            response=inline_serializer(
                name="AssignProgramEventAdminNotFound",
                fields={
                    "detail": serializers.CharField()
                }
            ),
            examples=[
                OpenApiExample(
                    name="Error - User not found",
                    description="No user found with the given email.",
                    value={"detail": "User not found."},
                    response_only=True
                ),
                OpenApiExample(
                    name="Error - Program not found",
                    description="No program found with the given id.",
                    value={"detail": "Program not found."},
                    response_only=True
                )
            ]
        ),
    },
    summary="Assign User to be a Program Event Admin in a specific Program.",
    description="Assigns a user as a program event admin if the user is active, hasn't been revoked permission, and hasn't already been granted permission.",
    tags=["16. Assign/Revoke Program Event Admin (by Organizational Admin & Organizational Super Admin)"]
)

revoke_program_event_admin_schema = extend_schema(
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "email": {
                    'type': 'string',
                    'format': 'email',
                    'description': 'Email of the user to revoke as program event admin.'
                }
            },
            "required": ['email']
        }
    },
    responses={
        200: OpenApiResponse(
            description="Success",
            response=ProgramEventAdmin_AdminSerializer,
        ),
        400: OpenApiResponse(
            description="Bad Request",
            response=inline_serializer(
                name="RevokeProgramEventAdminBadRequest",
                fields={
                    "error": serializers.CharField()
                }
            ),
            examples=[
                OpenApiExample(
                    name="Error - Program archived",
                    description="The program is archived.",
                    value={"error": "Program is archived."},
                    response_only=True
                ),
                OpenApiExample(
                    name="Error - User is banned",
                    description="The user is banned and cannot be revoked.",
                    value={"error": "User is banned."},
                    response_only=True
                ),
                OpenApiExample(
                    name="Error - Already revoked",
                    description="The user has already been revoked as program admin.",
                    value={"error": "User has already been revoked as program admin."},
                    response_only=True
                )
            ]
        ),
        404: OpenApiResponse(
            description="Not Found",
            response=inline_serializer(
                name="RevokeProgramEventAdminNotFound",
                fields={
                    "detail": serializers.CharField()
                }
            ),
            examples=[
                OpenApiExample(
                    name="Error - User not found",
                    description="No user found with the given email.",
                    value={"detail": "User not found."},
                    response_only=True
                ),
                OpenApiExample(
                    name="Error - Program not found",
                    description="No program found with the given id.",
                    value={"detail": "Program not found."},
                    response_only=True
                ),
                OpenApiExample(
                    name="Error - Program admin not assigned",
                    description="No program admin found for the given user in this program.",
                    value={"detail": "Program admin not assigned."},
                    response_only=True
                )
            ]
        ),
    },
    summary="Revoke User as a Program Event Admin from a specific Program.",
    description="Revokes a user as a program event admin if the user is active, and hasn't already been revoked permission.",
    tags=["16. Assign/Revoke Program Event Admin (by Organizational Admin & Organizational Super Admin)"]
)



# 17

get_all_program_event_admins_schema = extend_schema(
    responses=inline_serializer(
        name="ViewAllProgramEventAdminsInProgram",
        fields={
            "count": serializers.IntegerField(),
            "next": serializers.CharField(allow_null=True),
            "previous": serializers.CharField(allow_null=True),
            "results": ProgramEventAdmin_AdminSerializer(many=True)
        }
    ),
    summary="View All Program Event Admins in a specific Program.",
    description="Retrieves a paginated list of all program event admins in a specific program.",
    tags=["17. View Program Event Admins in a specific Program (by Program Admin & Organizational Admin & Organizational Super Admin)"]
)

get_user_program_event_admins_schema = extend_schema(
    methods=["GET"],
    parameters=[
        OpenApiParameter(
            name="email",
            description="Email address of the user to filter program admins by.",
            required=True,
            type=str,
            location=OpenApiParameter.QUERY
        )
    ],
    responses={
        200: ProgramEventAdmin_AdminSerializer(),
        404: OpenApiResponse(
            description="GetUserProgramEventAdminNotFound",
            response=inline_serializer(
                name="GetUserProgramEventAdminNotFound",
                fields={"detail": serializers.CharField()},
            ),
            examples=[
                OpenApiExample(
                    name="Program Admin not Assigned",
                    description="User not assigned as program admin in this program.",
                    value={"detail": "User is not assigned as program admin in this organization."},
                    response_only=True,
                    status_codes=["404"]
                ),
                OpenApiExample(
                    name="User not found",
                    description="User not found.",
                    value={"detail": "User not found."},
                    response_only=True,
                    status_codes=["404"]
                ),
                OpenApiExample(
                    name="Program not found",
                    description="Program not found.",
                    value={"detail": "Program not found."},
                    response_only=True,
                    status_codes=["404"]
                ),
            ]
        ),
    },
    description="Retrieves the data of the user assigned as program event admin in a specific program.",
    summary="View a specific Program Event Admin in a specific Program by providing email (faster retrieval).",
    tags=["17. View Program Event Admins in a specific Program (by Program Admin & Organizational Admin & Organizational Super Admin)"]
)

# 18

update_program_event_admin_schema = extend_schema(
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "email": {
                    'type': 'string',
                    'format': 'email',
                    'description': 'Email of the user to update as program event admin.'
                },
                "role": {
                    'type': 'string',
                    'description': 'Role of the user (Optional).'
                },
                "can_add_another_admin": {
                    'type': 'boolean',
                    'description': 'Can add another admin (Optional).'
                },
                "can_archive_program": {
                    'type': 'boolean',
                    'description': 'Can archive program (Optional).'
                },
                "can_archive_event": {
                    'type': 'boolean',
                    'description': 'Can archive event (Optional).'
                },
                "can_add_event_organizer": {
                    'type': 'boolean',
                    'description': 'Can add event organizer (Optional).'
                },
                "can_remove_event_organizer_from_program": {
                    'type': 'boolean',
                    'description': 'Can remove event organizer from program (Optional).'
                },
                "can_change_attendance_validity": {
                    'type': 'boolean',
                    'description': 'Can change attendance validity (Optional).'
                },
                "can_create_events": {
                    'type': 'boolean',
                    'description': 'Can create events (Optional).'
                },
                "can_conclude_events": {
                    'type': 'boolean',
                    'description': 'Can conclude events (Optional).'
                }
            },
            "required": ['email']
        }
    },
    responses={
        200: OpenApiResponse(
            description="Success",
            response=ProgramEventAdmin_AdminSerializer,
        ),
        400: OpenApiResponse(
            description="Bad Request",
            response=inline_serializer(
                name="UpdateProgramEventAdminBadRequest",
                fields={
                    "error": serializers.CharField()
                }
            ),
            examples=[
                OpenApiExample(
                    name="Error - Program archived",
                    description="The program is archived.",
                    value={"error": "Program is archived."},
                    response_only=True
                ),
                OpenApiExample(
                    name="Error - Email is required",
                    description="The email is required to identify the admin.",
                    value={"error": "Email is required to identify the admin."},
                    response_only=True
                ),
                OpenApiExample(
                    name="Error - User is banned",
                    description="The user is banned and cannot be updated.",
                    value={"error": "User is banned."},
                    response_only=True
                ),
                OpenApiExample(
                    name="Error - Revoked",
                    description="The user has been revoked as program admin.",
                    value={"error": "User has been revoked as program admin."},
                    response_only=True
                ),
            ]
        ),
        404: OpenApiResponse(
            description="Not Found",
            response=inline_serializer(
                name="UpdateProgramEventAdminNotFound",
                fields={
                    "detail": serializers.CharField()
                }
            ),
            examples=[
                OpenApiExample(
                    name="Error - User not found",
                    description="No user found with the given email.",
                    value={"detail": "User not found."},
                    response_only=True
                ),
                OpenApiExample(
                    name="Error - Program not found",
                    description="No program found with the given id.",
                    value={"detail": "Program not found."},
                    response_only=True
                ),
                OpenApiExample(
                    name="Error - Program admin not assigned",
                    description="No program admin found for the given user in this program.",
                    value={"detail": "Program admin not assigned."},
                    response_only=True
                )
            ]
        ),
    },
    summary="Update User as a Program Event Admin in a specific Program.",
    description="Updates a user's program event admin permissions if the user is active and hasn't been revoked permission. Only send the fields you need to change since this is a PATCH request.",
    tags=["18. Update Program Event Admin (by Organizational Admin & Organizational Super Admin)"]
)
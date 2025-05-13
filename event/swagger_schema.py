from drf_spectacular.utils import OpenApiResponse, OpenApiExample, inline_serializer, extend_schema
from rest_framework import serializers
from .serializers import EventSerializer, AttendanceSerializer, AttendanceAdminSerializer
from program.serializers import ProgramSerializer
from organization.serializers import OrganizationSerializer

# 19

create_event_schema = extend_schema(
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'title': {
                    'type': 'string',
                    'description': 'Title of the event.'
                },
                'description': {
                    'type': 'string',
                    'description': 'Detailed description of the event.'
                }
            },
            'required': ['title']
        }
    },
    responses={
        201: EventSerializer,
        400: OpenApiResponse(
            description="Validation error or inactive program.",
            response=inline_serializer(
                name="CreateEventBadRequest",
                fields={
                    "error": serializers.CharField(required=False),
                    "title": serializers.ListField(
                        child=serializers.CharField(), required=False
                    ),
                    "description": serializers.ListField(
                        child=serializers.CharField(), required=False
                    )
                }
            ),
            examples=[
                OpenApiExample(
                    name="Program is archived",
                    value={"error": "Program is archived."},
                    response_only=True
                ),
                OpenApiExample(
                    name="Missing title",
                    value={"title": ["This field is required."]},
                    response_only=True
                ),
                OpenApiExample(
                    name="Missing description",
                    value={"description": ["This field is required."]},
                    response_only=True
                )
            ]
        ),
        404: OpenApiResponse(
            description="Program not found.",
            response=inline_serializer(
                name="CreateEventNotFound",
                fields={
                    "detail": serializers.CharField()
                }
            ),
            examples=[
                OpenApiExample(
                    name="Program missing",
                    value={"detail": "Program not found."},
                    response_only=True
                )
            ]
        )
    },
    summary="Create Event",
    description="Create a new event under a specific program. The program ID must be passed in the URL as `program_pk`.",
    tags=["19. Create/View/Conclude/Archive/Reactivate Event (by Program Event Admin & Organizational Admin & Organizational Super Admin)"]
)


list_program_events_schema = extend_schema(
    summary="List Program Events",
    description=(
        "Lists all events created by the specified program.\n\n"
    ),
    tags=["19. Create/View/Conclude/Archive/Reactivate Event (by Program Event Admin & Organizational Admin & Organizational Super Admin)"],
    responses={
        200: EventSerializer(many=True),
        404: inline_serializer(
            name="ListProgramEvents404",
            fields={"detail": serializers.CharField(default="No Program matches the given query.")}
        ),
    }
)

archive_event_schema = extend_schema(
    summary="Archive an Event",
    description=(
        "Archives the specified event by setting is_archived to True, also setting the archived_at timestamp, "
        "and recording the user who performed the action.\n\n"
    ),
    tags=["19. Create/View/Conclude/Archive/Reactivate Event (by Program Event Admin & Organizational Admin & Organizational Super Admin)"],
    request=None,  
    responses={
        200: EventSerializer,
        400: OpenApiResponse(
            description="Bad Request - if already archived",
            response=inline_serializer(
                name="ArchiveEvent400",
                fields={"error": serializers.CharField()},
            ),
            examples=[
                OpenApiExample(
                    name="Already Archived",
                    description="Event is already archived and cannot be archived again.",
                    value={"error": "Event is already archived."},
                    response_only=True,
                    status_codes=["400"]
                )
            ]
        ),
        403: inline_serializer(
            name="ArchiveEvent403",
            fields={"detail": serializers.CharField(default="You do not have permission to perform this action.")}
        ),
        404: inline_serializer(
            name="ArchiveEvent404",
            fields={"detail": serializers.CharField(default="No Event matches the given query.")}
        ),
    }
)


conclude_event_schema = extend_schema(
    summary="Conclude an Event",
    description=(
        "Concludes the specified event by setting is_concluded to True, also setting the concluded_at timestamp, "
        "and recording the user who performed the action.\n\n"
    ),
    tags=["19. Create/View/Conclude/Archive/Reactivate Event (by Program Event Admin & Organizational Admin & Organizational Super Admin)"],
    request=None,  
    responses={
        200: EventSerializer,
        400: OpenApiResponse(
            description="Bad Request",
            response=inline_serializer(
                name="ConcludeEvent400",
                fields={"error": serializers.CharField()},
            ),
            examples=[
                OpenApiExample(
                    name="Already Concluded",
                    description="Event is already concluded and cannot be concluded again.",
                    value={"error": "Event is already concluded."},
                    response_only=True,
                    status_codes=["400"]
                ),
                OpenApiExample(
                    name="Event is archived",
                    description="Event is already archived and cannot be concluded.",
                    value={"error": "Event is already archived."},
                    response_only=True,
                    status_codes=["400"]
                )
            ]
        ),
        403: inline_serializer(
            name="ArchiveEvent403",
            fields={"detail": serializers.CharField(default="You do not have permission to perform this action.")}
        ),
        404: inline_serializer(
            name="ArchiveEvent404",
            fields={"detail": serializers.CharField(default="No Event matches the given query.")}
        ),
    }
)


reactivate_event_schema = extend_schema(
    summary="Reactivate an Event",
    description=(
        "Reactivates the specified event by setting is_archived to False, also setting the reactivated_at timestamp, "
        "and recording the user who performed the action.\n\n"
    ),
    tags=["19. Create/View/Conclude/Archive/Reactivate Event (by Program Event Admin & Organizational Admin & Organizational Super Admin)"],
    request=None,  
    responses={
        200: EventSerializer,
        400: OpenApiResponse(
            description="Bad Request",
            response=inline_serializer(
                name="ReactivateEvent400",
                fields={"error": serializers.CharField()},
            ),
            examples=[
                OpenApiExample(
                    name="Not Archived",
                    description="Event is not archived and cannot be reactivated.",
                    value={"error": "Event is not archived."},
                    response_only=True,
                    status_codes=["400"]
                )
            ]
        ),
        403: inline_serializer(
            name="ReactivateEvent403",
            fields={"detail": serializers.CharField(default="You do not have permission to perform this action.")}
        ),
        404: inline_serializer(
            name="ReactivateEvent404",
            fields={"detail": serializers.CharField(default="No Event matches the given query.")}
        ),
    }
)

# 20

get_event_by_short_code_schema = extend_schema(
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "short_code": {
                    'type': 'string',
                    'format': 'email',
                    'description': 'Short code of the event.'
                },
            },
            "required": ['short_code']
        }
    },
    responses={
        200: OpenApiResponse(
            description="Success",
            response=EventSerializer,
        ),
        400: OpenApiResponse(
            description="Bad Request",
            response=inline_serializer(
                name="GetEventByShortCodeBadRequest",
                fields={
                    "error": serializers.CharField()
                }
            ),
            examples=[
                OpenApiExample(
                    name="Error - Short code is required",
                    description="The short code is required.",
                    value={"error": "Short code is required."},
                    response_only=True
                ),
            ]
        ),
        404: OpenApiResponse(
            description="Not Found",
            response=inline_serializer(
                name="GetEventByShortCodeNotFound",
                fields={
                    "detail": serializers.CharField()
                }
            ),
            examples=[
                OpenApiExample(
                    name="Error - Event not found",
                    description="No event found with the given short code.",
                    value={"detail": "Event not found."},
                    response_only=True
                ),
            ]
        ),
    },
    summary="Get Event by Short Code",
    description="Get an event by its short code.",
    tags=["20. Get Event by Short Code (by Attendee)"]
)

# 21

create_attendance_schema = extend_schema(
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'display_name': {
                    'type': 'string',
                    'description': 'Display name of the attendee i.e. ID of attendee in organization.'
                },
                "signature_base64": {"type": "string", "example": "data:image/png;base64,iVBO..."},
            },
            'required': ['display_name', "signature_base64"]
        }
    },
    responses={
        201: AttendanceSerializer,
        400: OpenApiResponse(
            description="Archived event.",
            response=inline_serializer(
                name="CreateAttendanceBadRequest",
                fields={
                    "error": serializers.CharField(required=False),
                    "display_name": serializers.ListField(
                        child=serializers.CharField(), required=False
                    ),
                }
            ),
            examples=[
                OpenApiExample(
                    name="Event is archived",
                    value={"error": "Event is archived."},
                    response_only=True
                )
            ]
        ),
        404: OpenApiResponse(
            description="Event not found.",
            response=inline_serializer(
                name="CreateEventNotFound",
                fields={
                    "detail": serializers.CharField()
                }
            ),
            examples=[
                OpenApiExample(
                    name="Event not found",
                    value={"detail": "Event not found."},
                    response_only=True
                )
            ]
        )
    },
    summary="Create Attendance",
    description="Create a new attendance under a specific event. The event ID must be passed in the URL as `event_pk`. Display name is optional",
    tags=["21. Create Attendance (by Attendee)"]
)

# 22


list_my_attendances_schema = extend_schema(
    summary="List All My Attendances",
    description=(
        "Lists all attendances created by the specified attendee.\n\n"
    ),
    tags=["22. List Attendances (by Attendee)"],
    responses={
        200: AttendanceSerializer(many=True)
    }
)


list_attended_programs_schema = extend_schema(
    summary="List Attended Programs",
    description=(
        "Lists all programs attended by the specified attendee while attending events created under the Programs.\n\n"
    ),
    tags=["22. List Attendances (by Attendee)"],
    responses={
        200: ProgramSerializer(many=True)
    }
)


list_attended_organizations_schema = extend_schema(
    summary="List Attended Organizations",
    description=(
        "Lists all organizations attended by the specified attendee while attending events created under programs created by the Organizations.\n\n"
    ),
    tags=["22. List Attendances (by Attendee)"],
    responses={
        200: OrganizationSerializer(many=True)
    }
)

# 23

update_display_name_schema = extend_schema(
    summary="Update Display Name",
    description=(
        "Updates the display name of the specified attendance.\n\n"
    ),
    tags=["23. Update Display Name (by Attendee)"],
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'display_name': {
                    'type': 'string',
                    'description': 'Display name of the attendee i.e. ID of attendee in organization.'
                },
            },
            'required': ['display_name']
        }
    },
    responses={
        200: AttendanceSerializer
    }
)

# 24

event_attendees_schema = extend_schema(
    summary="Get Event Attendees",
    description=(
        "Lists all attendees of the specified event.\n\n"
    ),
    tags=["24. Get Event Attendees (by Program Event Admin & Organizational Admin & Organizational Super Admin)"],
    responses={
        200: AttendanceSerializer(many=True)
    }
)

# 25

invalidate_attendance_schema = extend_schema(
    summary="Invalidate Attendance",
    description=(
        "Invalidates the specified attendance.\n\n"
    ),
    responses={
        200: AttendanceAdminSerializer
    },
    tags=["25. Invalidate/Revalidate Attendance (by Program Event Admin & Organizational Admin & Organizational Super Admin)"]
)

revalidate_attendance_schema = extend_schema(
    summary="Revalidate Attendance",
    description=(
        "Revalidates the specified attendance.\n\n"
    ),
    responses={
        200: AttendanceAdminSerializer
    },
    tags=["25. Invalidate/Revalidate Attendance (by Program Event Admin & Organizational Admin & Organizational Super Admin)"]
)
from drf_spectacular.utils import OpenApiResponse, OpenApiExample, inline_serializer, extend_schema
from rest_framework import serializers
from .serializers import UserCreateSerializer, UserSerializer 

# 1
create_schema = extend_schema(
    request=UserCreateSerializer,
    responses={
        201: UserSerializer,
        400: OpenApiResponse(
            description="Bad Request",
            response=inline_serializer(
                name="UserCreateBadRequest",
                fields={
                    "error": serializers.CharField()
                }
            ),
            examples=[
                OpenApiExample(
                    name="Error - Invalid input",
                    description="Invalid input provided",
                    value={
                        "email": ["This field is required."],
                        "phone": ["This field is required."],
                        "name": ["This field is required."],
                        "signature_base64": ["Invalid base64 signature format. Must start with 'data:image'."]
                    }
                ),
            ]
        ),
    },
    description="Create a new user account with email, phone, name, and signature.",
    tags=["1. Register and login"]
)

email_login_schema = extend_schema(
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "email": {"type": "string", "example": "user@example.com"},
                "signature_base64": {"type": "string", "example": "data:image/png;base64,iVBO..."},
            },
            "required": ["email", "signature_base64"],
        }
    },
    responses={
        200: OpenApiResponse(
            description="Success",
            response=inline_serializer(
                name="RegisterSuccess",
                fields={
                    "message": serializers.CharField(
                        help_text="Returns access and refresh token."
                    )
                }
            ),
            examples=[
                OpenApiExample(
                    name="Success Example",
                    value={
                        "user": {
                            "id": 1,
                            "name": "john doe",
                            "phone": "111",
                            "email": "john@example.com"
                        },
                        "access_token": "abcd...",
                        "refresh_token": "efgh...",
                    },
                    response_only=True
                )
            ]
        ),
        400: OpenApiResponse(
            description="Bad Request",
            response=inline_serializer(
                name="EmailLoginBadRequest",
                fields={
                    "error": serializers.CharField()
                }
            ),
            examples=[
                OpenApiExample('Signature mismatch', value={"error": "Signature mismatch. Please try again!"}),
                OpenApiExample('Signature invalid', value={"error": "Signature missing or invalid."}),
            ]
        ),
        404: OpenApiResponse(
            description="Bad Request",
            response=inline_serializer(
                name="EmailLoginNotFound",
                fields={
                    "error": serializers.CharField()
                }
            ),
            examples=[
                OpenApiExample('User not found', value={"error": "User not found."}),
            ]
        ),
    },
    description="Login using email and base64-encoded signature comparison.",
    tags=["1. Register and login"]
)

phone_login_schema = extend_schema(
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "phone": {"type": "string", "example": "+251900000000"},
                "signature_base64": {"type": "string", "example": "data:image/png;base64,iVBO..."},
            },
            "required": ["phone", "signature_base64"],
        }
    },
    responses={
        200: OpenApiResponse(
            description="Success",
            response=inline_serializer(
                name="RegisterSuccess",
                fields={
                    "message": serializers.CharField(
                        help_text="Returns access and refresh token."
                    )
                }
            ),
            examples=[
                OpenApiExample(
                    name="Success Example",
                    value={
                        "user": {
                            "id": 1,
                            "name": "john doe",
                            "phone": "111",
                            "email": "john@example.com"
                        },
                        "access_token": "abcd...",
                        "refresh_token": "efgh...",
                    },
                    response_only=True
                )
            ]
        ),
        400: OpenApiResponse(
            description="Bad Request",
            response=inline_serializer(
                name="PhoneLoginBadRequest",
                fields={
                    "error": serializers.CharField()
                }
            ),
            examples=[
                OpenApiExample('Signature mismatch', value={"error": "Signature mismatch. Please try again!"}),
                OpenApiExample('Signature invalid', value={"error": "Signature missing or invalid."}),
            ]
        ),
        404: OpenApiResponse(
            description="Bad Request",
            response=inline_serializer(
                name="PhoneLoginNotFound",
                fields={
                    "error": serializers.CharField()
                }
            ),
            examples=[
                OpenApiExample('User not found', value={"error": "User not found."}),
                        ]
        ),
    },
    description="Login using phone number and base64-encoded signature comparison.",
    tags=["1. Register and login"]
)
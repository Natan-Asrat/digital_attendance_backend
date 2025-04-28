from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserCreateSerializer, UserSerializer  # Assuming UserCreateSerializer is the correct one to use
from rest_framework.decorators import action
from .utils import calculate_signature_similarity
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from rest_framework import serializers
from drf_spectacular.utils import inline_serializer

class UserViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    @extend_schema(
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
    def create(self, request, *args, **kwargs):
        """Override the create method to handle custom logic."""
        serializer = UserCreateSerializer(data=request.data)
        print("hi", request.data)
        if serializer.is_valid():
            user = serializer.save() 
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        
        # If the data is invalid, return a bad request response with the errors
        print("errors", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @extend_schema(
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
            200: UserSerializer,
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
    @action(detail=False, methods=['POST'])
    def email_login(self, request, *args, **kwargs):
        """Login using email and signature verification."""
        email = request.data.get('email')
        signature_base64 = request.data.get('signature_base64')
        
        # Retrieve the user by email
        user = User.objects.filter(email=email).first()
        if user is None:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check the signature similarity
        base64_existing_signature = user.signaturebase64
        if signature_base64 and base64_existing_signature:
            similarity = calculate_signature_similarity(signature_base64, base64_existing_signature)
            print("Signature similarity:", similarity)

            # If similarity is greater than 50%, authenticate user and issue tokens
            if similarity >= 0.5:
                # Generate access and refresh tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return Response({
                    "user": UserSerializer(user).data,
                    "access_token": access_token,
                    "refresh_token": str(refresh),
                }, status=status.HTTP_200_OK)

            return Response({
                "error": "Signature mismatch. Please try again!"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"error": "Signature missing or invalid."}, status=status.HTTP_400_BAD_REQUEST)
    @extend_schema(
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
            200: UserSerializer,
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
    @action(detail=False, methods=['POST'])
    def phone_login(self, request, *args, **kwargs):
        """Login using phone number and signature verification."""
        phone = request.data.get('phone')
        signature_base64 = request.data.get('signature_base64')
        
        # Retrieve the user by phone number
        user = User.objects.filter(phone=phone).first()
        if user is None:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check the signature similarity
        base64_existing_signature = user.signaturebase64
        if signature_base64 and base64_existing_signature:
            similarity = calculate_signature_similarity(signature_base64, base64_existing_signature)
            print("Signature similarity:", similarity)

            # If similarity is greater than 50%, authenticate user and issue tokens
            if similarity >= 0.5:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return Response({
                    "user": UserSerializer(user).data,
                    "access_token": access_token,
                    "refresh_token": str(refresh),
                }, status=status.HTTP_200_OK)

            return Response({
                "error": "Signature mismatch. Please try again!"
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "Signature missing or invalid."}, status=status.HTTP_400_BAD_REQUEST)
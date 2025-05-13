from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserCreateSerializer, UserSerializer  # Assuming UserCreateSerializer is the correct one to use
from rest_framework.decorators import action
from .utils import calculate_signature_similarity
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from .swagger_schema import (
    create_schema, email_login_schema, phone_login_schema
)
from django.conf import settings

class UserSimpleViewset(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_permissions(self):
        if self.action in ['create', 'email_login', 'phone_login']:
            return [AllowAny()]
        return [IsAuthenticated()]

    @create_schema
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
    
    @email_login_schema
    @action(detail=False, methods=['POST'])
    def email_login(self, request, *args, **kwargs):
        """Login using email and signature verification."""
        email = request.data.get('email')
        signature_base64 = request.data.get('signature_base64')
        
        # Retrieve the user by email
        user = User.objects.filter(email=email).first()
        if user is None:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check the signature similarity
        base64_existing_signature = user.signaturebase64
        if signature_base64 and base64_existing_signature:
            similarity = calculate_signature_similarity(signature_base64, base64_existing_signature)
            print("Signature similarity:", similarity)

            # If similarity is greater than 50%, authenticate user and issue tokens
            if similarity >= settings.SIGNATURE_THRESHOLD:
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
    
    @phone_login_schema
    @action(detail=False, methods=['POST'])
    def phone_login(self, request, *args, **kwargs):
        """Login using phone number and signature verification."""
        phone = request.data.get('phone')
        signature_base64 = request.data.get('signature_base64')
        
        # Retrieve the user by phone number
        user = User.objects.filter(phone=phone).first()
        if user is None:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check the signature similarity
        base64_existing_signature = user.signaturebase64
        if signature_base64 and base64_existing_signature:
            similarity = calculate_signature_similarity(signature_base64, base64_existing_signature)
            print("Signature similarity:", similarity)

            # If similarity is greater than 50%, authenticate user and issue tokens
            if similarity >= settings.SIGNATURE_THRESHOLD:
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
from rest_framework.viewsets import GenericViewSet
from .models import Organization
from .serializers import OrganizationSerializer
from rest_framework.decorators import action
from account.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from drf_spectacular.utils import OpenApiResponse, extend_schema, OpenApiExample, inline_serializer
from django.utils import timezone
from rest_framework.permissions import AllowAny
from .swagger_schema import (
    assign_organization_super_admin_schema, 
    revoke_organization_super_admin_schema, 
    assign_staff_schema, revoke_staff_schema
)

# Create your views here.
class OrganizationViewset(GenericViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
    permission_classes = [AllowAny]

    @assign_organization_super_admin_schema
    @action(detail=False, methods=['post'])
    def assign_organization_super_admin(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            assigned_user = User.objects.get(email=email)
            if not assigned_user.is_active:
                return Response({"error": "User is banned."}, status=status.HTTP_400_BAD_REQUEST)
            if assigned_user.revoked_organizational_permission_at is not None:
                return Response({"error": "User has been revoked organizational super admin permission."}, status=status.HTTP_400_BAD_REQUEST)
            if assigned_user.granted_organizational_permission_at is not None:
                return Response({"error": "User has already been granted organizational super admin permission."}, status=status.HTTP_400_BAD_REQUEST)
            print("req", request.data)

            assigned_user.can_create_organizations = True
            assigned_user.granted_organizational_permission_by = request.user
            assigned_user.granted_organizational_permission_at = timezone.now()
            assigned_user.save()
            return Response({"message": "User assigned as organizational super admin successfully."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @revoke_organization_super_admin_schema
    @action(detail=False, methods=['post'])
    def revoke_organization_super_admin(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            assigned_user = User.objects.get(email=email)
            if not assigned_user.is_active:
                return Response({"error": "User is banned."}, status=status.HTTP_400_BAD_REQUEST)
            if assigned_user.revoked_organizational_permission_at is not None:
                return Response({"error": "User has already been revoked organizational super admin permission."}, status=status.HTTP_400_BAD_REQUEST)
            assigned_user.can_create_organizations = False
            assigned_user.revoked_organizational_permission_by = request.user
            assigned_user.revoked_organizational_permission_at = timezone.now()
            assigned_user.save()
            return Response({"message": "User has been revoked organizational super admin permission successfully."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @assign_staff_schema
    @action(detail=False, methods=['post'])
    def assign_staff(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            assigned_user = User.objects.get(email=email)
            if assigned_user.is_superuser:
                return Response({"error": "You are not allowed to alter this account"}, status=status.HTTP_403_FORBIDDEN)
            if not assigned_user.is_active:
                return Response({"error": "User is banned."}, status=status.HTTP_400_BAD_REQUEST)
            if assigned_user.revoked_staff_status_at is not None:
                return Response({"error": "User has been revoked from Staff permission."}, status=status.HTTP_400_BAD_REQUEST)
            if assigned_user.is_staff or assigned_user.granted_staff_status_at is not None:
                return Response({"error": "User has already been granted Staff permission."}, status=status.HTTP_400_BAD_REQUEST)

            assigned_user.is_staff = True
            assigned_user.granted_staff_status_by = request.user
            assigned_user.granted_staff_status_at = timezone.now()
            assigned_user.save()
            return Response({"message": "User assigned as Staff successfully."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @revoke_staff_schema
    @action(detail=False, methods=['post'])
    def revoke_staff(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            assigned_user = User.objects.get(email=email)
            if assigned_user.is_superuser:
                return Response({"error": "You are not allowed to alter this account"}, status=status.HTTP_403_FORBIDDEN)
            if not assigned_user.is_active:
                return Response({"error": "User is banned."}, status=status.HTTP_400_BAD_REQUEST)
            if assigned_user.revoked_staff_status_at is not None:
                return Response({"error": "User has already been revoked Staff permissions."}, status=status.HTTP_400_BAD_REQUEST)

            assigned_user.is_staff = False
            assigned_user.revoked_staff_status_by = request.user
            assigned_user.revoked_staff_status_at = timezone.now()
            assigned_user.save()
            return Response({"message": "User has been revoked Staff permissions successfully."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
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
# Create your views here.
class OrganizationViewset(GenericViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
    
    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'user_id': {
                        'type': 'string',
                        'format': 'uuid',
                        'description': 'The ID of the user to assign as organization super admin.'
                    }
                },
                'required': ['user_id'],
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
        tags=["2. Assign/Revoke Organizational Super Admin"]
    )
    @action(detail=False, methods=['post'])
    def assign_organization_super_admin(self, request, *args, **kwargs):
        try:
            user_id = request.data.get('user_id')
            print("user", user_id)
            assigned_user = User.objects.get(id=user_id)
            print("got", assigned_user)
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
    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'user_id': {
                        'type': 'string',
                        'format': 'uuid',
                        'description': 'The ID of the user to revoke organization super admin permission from.'
                    }
                },
                'required': ['user_id'],
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
        tags=["2. Assign/Revoke Organizational Super Admin"]
    )

    @action(detail=False, methods=['post'])
    def revoke_organization_super_admin(self, request, *args, **kwargs):
        try:
            user_id = request.data.get('user_id')
            assigned_user = User.objects.get(id=user_id)
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

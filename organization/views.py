from rest_framework.viewsets import GenericViewSet
from .models import Organization
from .serializers import OrganizationSerializer
from rest_framework.decorators import action
from account.models import User
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from rest_framework.permissions import AllowAny
from .swagger_schema import (
    assign_organization_super_admin_schema, 
    revoke_organization_super_admin_schema, 
    assign_staff_schema, revoke_staff_schema,
    create_organization_schema, view_all_organizations_schema,
    view_active_organizations_schema,
    view_archived_organizations_schema,
    archive_organization_schema
)
from .serializers import OrganizationCreateSerializer, OrganizationSerializer, OrganizationAdminSerializer
from .pagination import CustomPageNumberPagination

# Create your views here.
class OrganizationViewset(GenericViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action in ['view_all_organizations', 'view_active_organizations', 'view_archived_organizations']:
            return OrganizationAdminSerializer
        elif self.action == 'create_organization':
            return OrganizationCreateSerializer
        return OrganizationSerializer


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
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
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
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @assign_staff_schema
    @action(detail=False, methods=['post'])
    def assign_staff(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            assigned_user = User.objects.get(email=email)
            if assigned_user.is_superuser:
                return Response({"detail": "You are not allowed to alter this account"}, status=status.HTTP_403_FORBIDDEN)
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
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @revoke_staff_schema
    @action(detail=False, methods=['post'])
    def revoke_staff(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            assigned_user = User.objects.get(email=email)
            if assigned_user.is_superuser:
                return Response({"detail": "You are not allowed to alter this account"}, status=status.HTTP_403_FORBIDDEN)
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
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @create_organization_schema
    @action(detail=False, methods=['post'])
    def create_organization(self, request, *args, **kwargs):
        serializer = OrganizationCreateSerializer(data=request.data)
        if serializer.is_valid():
            organization = serializer.save(created_by=request.user)
            return Response(OrganizationSerializer(organization).data, status=status.HTTP_201_CREATED)
        print("errors", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @archive_organization_schema
    @action(detail=True, methods=['post'])
    def archive_organization(self, request, pk=None):
        organization = self.get_object()
        if not organization.is_active:
            return Response({"error": "Organization is already archived."}, status=status.HTTP_400_BAD_REQUEST)
        organization.is_active = False
        organization.archived_by = request.user
        organization.archived_at = timezone.now()
        organization.save()
        return Response(OrganizationAdminSerializer(organization).data, status=status.HTTP_200_OK)

    @view_all_organizations_schema
    @action(detail=False, methods=['get'])
    def view_all_organizations_schema(self, request, *args, **kwargs):
        organizations = Organization.objects.filter(created_by=request.user).select_related('created_by', 'archived_by')
        paginated_queryset = self.paginate_queryset(organizations)
        if paginated_queryset is not None:
            serializer = self.get_serializer(paginated_queryset, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(organizations, many=True)
        return Response(serializer.data)

    @view_active_organizations_schema
    @action(detail=False, methods=['get'])
    def view_active_organizations(self, request, *args, **kwargs):
        organizations = Organization.objects.filter(created_by=request.user, is_active=True).select_related('created_by', 'archived_by')
        paginated_queryset = self.paginate_queryset(organizations)
        if paginated_queryset is not None:
            serializer = self.get_serializer(paginated_queryset, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(organizations, many=True)
        return Response(serializer.data)

    @view_archived_organizations_schema
    @action(detail=False, methods=['get'])
    def view_archived_organizations(self, request, *args, **kwargs):
        organizations = Organization.objects.filter(created_by=request.user, is_active=False).select_related('created_by', 'archived_by')
        paginated_queryset = self.paginate_queryset(organizations)
        if paginated_queryset is not None:
            serializer = self.get_serializer(paginated_queryset, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(organizations, many=True)
        return Response(serializer.data)

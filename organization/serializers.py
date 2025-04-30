from rest_framework.serializers import ModelSerializer
from account.serializers import UserSerializer
from .models import Organization, OrganizationAdmin
from rest_framework import serializers

class OrganizationCreateSerializer(ModelSerializer):
    class Meta:
        model = Organization
        fields = ['code', 'name']

class OrganizationAdminSerializer(ModelSerializer):
    created_by  = UserSerializer()
    archived_by = UserSerializer()
    class Meta:
        model = Organization
        fields = ['id', 'code', 'name', 'is_active', 'created_at', 'archived_at', 'created_by', 'archived_by']

class OrganizationSerializer(ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'code', 'name', 'is_active']


class AssignOrganizationAdminSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role = serializers.CharField(default=OrganizationAdmin.ROLE_DEFAULT)
    can_add_another_admin = serializers.BooleanField(default=OrganizationAdmin.CAN_ADD_ANOTHER_ADMIN)
    can_archive_organization = serializers.BooleanField(default=OrganizationAdmin.CAN_ARCHIVE_ORGANIZATION)
    can_change_attendance_validity = serializers.BooleanField(default=OrganizationAdmin.CAN_CHANGE_ATTENDANCE_VALIDITY)
    can_create_programs = serializers.BooleanField(default=OrganizationAdmin.CAN_CREATE_PROGRAMS)

class PatchOrganizationalAdminSerializer(serializers.Serializer):
    role = serializers.CharField(required=False)
    can_add_another_admin = serializers.BooleanField(required=False)
    can_archive_organization = serializers.BooleanField(required=False)
    can_change_attendance_validity = serializers.BooleanField(required=False)
    can_create_programs = serializers.BooleanField(required=False)

class OrganizationalAdmin_AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    organization = OrganizationSerializer()
    added_by = UserSerializer()
    removed_by = UserSerializer()
    class Meta:
        model = OrganizationAdmin
        fields = '__all__'
    
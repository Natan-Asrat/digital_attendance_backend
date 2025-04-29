from rest_framework.serializers import ModelSerializer
from account.serializers import UserSerializer
from .models import Organization

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
from rest_framework.serializers import ModelSerializer
from organization.serializers import OrganizationSerializer
from .models import Program, ProgramInvite, InvitedOrganizationProgram, ProgramSubscriber
from account.serializers import UserSerializer

class ProgramSerializer(ModelSerializer):
    organization = OrganizationSerializer()
    class Meta:
        model = Program
        fields = ['id', 'name', 'organization', 'is_active', 'created_at']

class ProgramAdminSerializer(ModelSerializer):
    created_by = UserSerializer()
    archived_by = UserSerializer()
    organization = OrganizationSerializer()
    class Meta:
        model = Program
        fields = '__all__'

class ProgramCreateSerializer(ModelSerializer):
    class Meta:
        model = Program
        fields = ['name']

class ProgramInviteSerializer(ModelSerializer):
    organization = OrganizationSerializer()
    program = ProgramSerializer()
    class Meta:
        model = ProgramInvite
        fields = ['id', 'organization', 'program', 'is_active', 'invited_at']


class ProgramInviteAdminSerializer(ModelSerializer):
    organization = OrganizationSerializer()
    program = ProgramSerializer()
    invited_by = UserSerializer()
    accepted_by = UserSerializer()
    rejected_by = UserSerializer()
    removed_by = UserSerializer()
    class Meta:
        model = ProgramInvite
        fields = '__all__'


class InvitedOrganizationProgramSerializer(ModelSerializer):
    organization = OrganizationSerializer()
    program = ProgramSerializer()
    class Meta:
        model = InvitedOrganizationProgram
        fields = ['id', 'organization', 'program', 'is_active', 'accepted_at', 'rejected_at', 'removed_at']

class InvitedOrganizationProgramAdminSerializer(ModelSerializer):
    organization = OrganizationSerializer()
    program = ProgramSerializer()
    invite = ProgramInviteSerializer()
    accepted_by = UserSerializer()
    rejected_by = UserSerializer()
    removed_by = UserSerializer()
    class Meta:
        model = InvitedOrganizationProgram
        fields = '__all__'


class ProgramSubscriberGetProgsSerializer(ModelSerializer):
    program = ProgramSerializer()
    class Meta:
        model = ProgramSubscriber
        fields = '__all__'


class ProgramSubscriberGetSubsSerializer(ModelSerializer):
    subscriber = UserSerializer()
    class Meta:
        model = ProgramSubscriber
        fields = '__all__'
    
from rest_framework.serializers import ModelSerializer
from organization.serializers import OrganizationSerializer
from .models import Program, ProgramInvite, InvitedOrganizationProgram, ProgramSubscriber, ProgramEventAdmin
from account.serializers import UserSerializer
from rest_framework import serializers

class ProgramSerializer(ModelSerializer):
    organization = OrganizationSerializer()
    class Meta:
        model = Program
        fields = ['id', 'name', 'organization', 'is_active', 'created_at']

class ProgramListNestedSerializer(ModelSerializer):
    organization = OrganizationSerializer()
    created_by = UserSerializer()
    archived_by = UserSerializer()
    class Meta:
        model = Program
        fields = ['id', 'name', 'organization', 'is_active', 'created_at', 'created_by', 'archived_by', 'archived_at']

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
    
class AssignProgramEventAdminSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role = serializers.CharField(default=ProgramEventAdmin.ROLE_DEFAULT)
    can_add_another_admin = serializers.BooleanField(default=ProgramEventAdmin.CAN_ADD_ANOTHER_ADMIN)
    can_archive_program = serializers.BooleanField(default=ProgramEventAdmin.CAN_ARCHIVE_PROGRAM)
    can_archive_event = serializers.BooleanField(default=ProgramEventAdmin.CAN_ARCHIVE_EVENT)
    can_add_event_organizer = serializers.BooleanField(default=ProgramEventAdmin.CAN_ADD_EVENT_ORGANIZER)
    can_remove_event_organizer_from_program = serializers.BooleanField(default=ProgramEventAdmin.CAN_REMOVE_EVENT_ORGANIZER_FROM_PROGRAM)
    can_change_attendance_validity = serializers.BooleanField(default=ProgramEventAdmin.CAN_CHANGE_ATTENDANCE_VALIDITY)
    can_create_events = serializers.BooleanField(default=ProgramEventAdmin.CAN_CREATE_EVENTS)
    can_conclude_events = serializers.BooleanField(default=ProgramEventAdmin.CAN_CONCLUDE_EVENTS)

class PatchProgramEventAdminSerializer(serializers.Serializer):
    role = serializers.CharField(required=False)
    can_add_another_admin = serializers.BooleanField(required=False)
    can_archive_program = serializers.BooleanField(required=False)
    can_archive_event = serializers.BooleanField(required=False)
    can_add_event_organizer = serializers.BooleanField(required=False)
    can_remove_event_organizer_from_program = serializers.BooleanField(required=False)
    can_change_attendance_validity = serializers.BooleanField(required=False)
    can_create_events = serializers.BooleanField(required=False)
    can_conclude_events = serializers.BooleanField(required=False)

class ProgramEventAdmin_AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    program = ProgramSerializer()
    added_by = UserSerializer()
    removed_by = UserSerializer()
    class Meta:
        model = ProgramEventAdmin
        fields = '__all__'
    
from rest_framework import serializers
from .models import Event, Attendance
from program.serializers import ProgramSerializer
from account.serializers import UserSerializer

class EventSerializer(serializers.ModelSerializer):
    program = ProgramSerializer()
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'short_code', 'program', 'is_archived', 'is_concluded']

class AttendanceSerializer(serializers.ModelSerializer):
    event = EventSerializer()
    attendee = UserSerializer()
    class Meta:
        model = Attendance
        fields = ['id', 'event', 'attendee', 'display_name', 'valid', 'created_at']

class EventShortCodeSerializer(serializers.Serializer):
    short_code = serializers.CharField(max_length=100)

class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'description']

class EventAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class AttendanceAdminSerializer(serializers.ModelSerializer):
    event = EventSerializer()
    attendee = UserSerializer()
    validated_by = UserSerializer()
    invalidated_by = UserSerializer()
    class Meta:
        model = Attendance
        fields = '__all__'

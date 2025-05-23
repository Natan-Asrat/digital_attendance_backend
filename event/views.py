from rest_framework.viewsets import GenericViewSet
from .models import Event, Attendance
from .serializers import EventCreateSerializer, EventSerializer, AttendanceSerializer, EventAdminSerializer, AttendanceAdminSerializer
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny
from program.models import Program
from rest_framework.response import Response
from rest_framework import status
from .pagination import CustomPageNumberPagination
from rest_framework.decorators import action
from django.utils import timezone
from program.models import Program
from program.serializers import ProgramSerializer
from django.db.models import Q
from organization.models import Organization
from organization.serializers import OrganizationSerializer
from account.utils import calculate_signature_similarity
from django.conf import settings
from .swagger_schema import (
    create_event_schema,
    list_program_events_schema,
    archive_event_schema,
    conclude_event_schema,
    reactivate_event_schema,
    get_event_by_short_code_schema,
    create_attendance_schema,
    list_attended_programs_schema,
    list_attended_organizations_schema,
    list_my_attendances_schema,
    update_display_name_schema,
    event_attendees_schema,
    invalidate_attendance_schema,
    revalidate_attendance_schema
)
from .permissions import (
    EventViewSetPermissions,
    NestedEventViewSetPermissions,
    AttendanceViewSetPermissions,
    NestedAttendanceViewSetPermissions
)

# Create your views here.
class EventViewSet(GenericViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all().select_related('program', 'program__organization')
    permission_classes = [EventViewSetPermissions]
    pagination_class = CustomPageNumberPagination

    @get_event_by_short_code_schema
    @action(detail=False, methods=['post'])
    def event_by_short_code(self, request, *args, **kwargs):
        short_code = request.data.get('short_code')
        if short_code is None:
            return Response({"error": "Short code is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            event = Event.objects.select_related('program', 'program__organization').get(short_code=short_code)
            return Response(EventSerializer(event).data, status=status.HTTP_200_OK)
        except Event.DoesNotExist:
            return Response({"detail": "Event not found."}, status=status.HTTP_404_NOT_FOUND)
    
    @archive_event_schema
    @action(detail=True, methods=['post'])
    def archive_event(self, request, pk=None):
        event = self.get_object()
        if event.is_archived:
            return Response({"error": "Event is already archived."}, status=status.HTTP_400_BAD_REQUEST)
        event.is_archived = True
        event.archived_by = request.user
        event.archived_at = timezone.now()
        event.save()
        return Response(EventSerializer(event).data, status=status.HTTP_200_OK)

    @conclude_event_schema
    @action(detail=True, methods=['post'])
    def conclude_event(self, request, pk=None):
        event = self.get_object()
        if event.is_archived:
            return Response({"error": "Event is archived."}, status=status.HTTP_400_BAD_REQUEST)
        if event.is_concluded:
            return Response({"error": "Event is already concluded."}, status=status.HTTP_400_BAD_REQUEST)
        event.is_concluded = True
        event.concluded_by = request.user
        event.concluded_at = timezone.now()
        event.save()
        return Response(EventSerializer(event).data, status=status.HTTP_200_OK)

    @reactivate_event_schema
    @action(detail=True, methods=['post'])
    def reactivate_event(self, request, pk=None):
        event = self.get_object()
        if not event.is_archived:
            return Response({"error": "Event is not archived."}, status=status.HTTP_400_BAD_REQUEST)
        event.is_archived = False
        event.reactivated_by = request.user
        event.reactivated_at = timezone.now()
        event.save()
        return Response(EventSerializer(event).data, status=status.HTTP_200_OK)


class NestedEventViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all().select_related('program', 'program__organization')
    permission_classes = [NestedEventViewSetPermissions]
    pagination_class = CustomPageNumberPagination

    @list_program_events_schema
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def get_serializer_class(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return EventAdminSerializer
        return EventSerializer
    
    def get_queryset(self):
        program_id = self.kwargs.get('program_pk')
        return self.queryset.filter(program__id=program_id)
    
    @create_event_schema
    def create(self, request, *args, **kwargs):
        program_id = self.kwargs.get('program_pk')
        try:
            program = Program.objects.get(id=program_id)
            if not program.is_active:
                return Response({"error": "Program is archived."}, status=status.HTTP_400_BAD_REQUEST)

            serializer = EventCreateSerializer(data=request.data)
            if serializer.is_valid():
                event = serializer.save(program=program, created_by=request.user)
                return Response(EventSerializer(event).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Program.DoesNotExist:
            return Response({"detail": "Program not found."}, status=status.HTTP_404_NOT_FOUND)

class AttendanceViewset(GenericViewSet):
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects.all().select_related('event', 'event__program', 'event__program__organization', 'attendee', 'validated_by', 'invalidated_by')
    permission_classes = [AttendanceViewSetPermissions]
    pagination_class = CustomPageNumberPagination

    @list_attended_programs_schema
    @action(detail=False, methods=['get'])
    def my_attended_programs(self, request, *args, **kwargs):

        programs = Program.objects.select_related('organization').filter(
            event__attendance__attendee=request.user,
            event__attendance__valid=True
        ).distinct()

        page = self.paginate_queryset(programs)
        if page is not None:
            serializer = ProgramSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ProgramSerializer(programs, many=True)
        return Response(serializer.data)

    @list_attended_organizations_schema
    @action(detail=False, methods=['get'])
    def my_attended_organizations(self, request, *args, **kwargs):
        organizations = Organization.objects.filter(
            programs__event__attendance__attendee=request.user,
            programs__event__attendance__valid=True
        ).distinct()
        page = self.paginate_queryset(organizations)
        if page is not None:
            serializer = OrganizationSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = OrganizationSerializer(organizations, many=True)
        return Response(serializer.data)

    @list_my_attendances_schema
    @action(detail=False, methods=['get'])
    def my_attendances(self, request, *args, **kwargs):
        attendances = Attendance.objects.select_related('event', 'event__program', 'event__program__organization', 'attendee', 'validated_by', 'invalidated_by').filter(attendee=request.user)
        paginated_queryset = self.paginate_queryset(attendances)
        if paginated_queryset is not None:
            serializer = AttendanceSerializer(paginated_queryset, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)
    
    @invalidate_attendance_schema
    @action(detail=True, methods=['post'])
    def invalidate_attendance(self, request, pk=None):
        attendance = self.get_object()
        if not attendance.valid:
            return Response({"error": "Attendance is already invalidated."}, status=status.HTTP_400_BAD_REQUEST)
        attendance.valid = False
        attendance.invalidated_by = request.user
        attendance.invalidated_at = timezone.now()
        attendance.save()
        return Response(AttendanceAdminSerializer(attendance).data, status=status.HTTP_200_OK)
    
    @revalidate_attendance_schema
    @action(detail=True, methods=['post'])
    def revalidate_attendance(self, request, pk=None):
        attendance = self.get_object()
        if attendance.valid:
            return Response({"error": "Attendance is already validated."}, status=status.HTTP_400_BAD_REQUEST)
        attendance.valid = True
        attendance.validated_by = request.user
        attendance.validated_at = timezone.now()
        attendance.save()
        return Response(AttendanceAdminSerializer(attendance).data, status=status.HTTP_200_OK)
    
    @update_display_name_schema
    @action(detail=True, methods=['patch'])
    def update_display_name(self, request, pk=None):
        attendance = self.get_object()
        display_name = request.data.get('display_name')
        attendance.display_name = display_name
        attendance.save()
        return Response(AttendanceSerializer(attendance).data, status=status.HTTP_200_OK)

class NestedAttendanceViewset(ListModelMixin,CreateModelMixin, GenericViewSet):
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects.all().select_related('event', 'event__program', 'event__program__organization', 'attendee', 'validated_by', 'invalidated_by')
    permission_classes = [NestedAttendanceViewSetPermissions]
    pagination_class = CustomPageNumberPagination

    @event_attendees_schema
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return AttendanceAdminSerializer
        return AttendanceSerializer
    
    def get_queryset(self):
        event_id = self.kwargs.get('event_pk')
        return self.queryset.filter(event__id=event_id)
    
    @create_attendance_schema
    def create(self, request, *args, **kwargs):
        event_id = self.kwargs.get('event_pk')
        signature_base64 = request.data.get('signature_base64')
        user = request.user
        if user is None or not user.is_authenticated or user.signaturebase64 is None:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check the signature similarity
        base64_existing_signature = user.signaturebase64
        if signature_base64 and base64_existing_signature:
            similarity = calculate_signature_similarity(signature_base64, base64_existing_signature)
            print("Signature similarity:", similarity)

            # If similarity is greater than 50%, authenticate user and issue tokens
            if similarity < settings.SIGNATURE_THRESHOLD:
                return Response({
                    "error": "Signature mismatch. Please try again!"
                }, status=status.HTTP_400_BAD_REQUEST)
        try:
            event = Event.objects.get(id=event_id)
            if event.is_archived:
                return Response({"error": "Event is archived."}, status=status.HTTP_400_BAD_REQUEST)
            display_name = request.data.get('display_name')
            attendance = Attendance.objects.create(
                event=event,
                attendee=request.user,
                display_name=display_name,
                valid=True,
            )
            return Response(AttendanceSerializer(attendance).data, status=status.HTTP_201_CREATED)
        except Event.DoesNotExist:
            return Response({"detail": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

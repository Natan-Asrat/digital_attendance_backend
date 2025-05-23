from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from .models import Program, ProgramInvite, InvitedOrganizationProgram, ProgramSubscriber, ProgramEventAdmin
from .serializers import (
    ProgramSerializer,
    ProgramAdminSerializer,
    ProgramCreateSerializer,
    ProgramInviteSerializer,
    ProgramInviteAdminSerializer,
    InvitedOrganizationProgramSerializer,
    InvitedOrganizationProgramAdminSerializer,
    ProgramSubscriberGetSubsSerializer,
    ProgramSubscriberGetProgsSerializer,
    AssignProgramEventAdminSerializer,
    PatchProgramEventAdminSerializer,
    ProgramEventAdmin_AdminSerializer,
    ProgramListNestedSerializer
)
from .swagger_schema import (
    create_program_schema,
    archive_program_schema,
    list_organization_programs_schema,
    list_organization_associated_programs_schema,
    list_organization_invited_programs_schema,
    invite_organization_schema,
    undo_invite_organization_schema,
    accept_invite_schema,
    reject_invite_schema,
    list_program_invites_schema,
    list_organizations_invites_schema,
    leave_program_schema,
    subscribe_program_schema,
    unsubscribe_program_schema,
    my_subscribed_programs_schema,
    list_subscribers_in_program_schema,
    list_subscribed_programs_schema,
    assign_program_event_admin_schema,
    revoke_program_event_admin_schema,
    get_all_program_event_admins_schema,
    get_user_program_event_admins_schema,
    update_program_event_admin_schema

)
from .pagination import CustomPageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from organization.models import Organization
from account.models import User
from django.utils import timezone
from .permissions import (
    ProgramViewsetPermissions,
    ProgramInviteViewsetPermissions,
    ProgramInvitedOrganizationViewsetPermissions,
    NestedOrganizationInviteViewsetPermissions,
    NestedSubscribersViewsetPermissions,
    NestedSubscribedProgramsViewsetPermissions,
    NestedProgramInviteViewsetPermissions,
)

# Create your views here.
class ProgramSimpleViewset(GenericViewSet):
    serializer_class = ProgramSerializer
    queryset = Program.objects.all()
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination


class ProgramViewset(GenericViewSet):
    serializer_class = ProgramSerializer
    queryset = Program.objects.all()
    permission_classes = [ProgramViewsetPermissions]
    pagination_class = CustomPageNumberPagination

    @create_program_schema
    @action(detail=False, methods=['post'])
    def create_program(self, request, *args, **kwargs):
        try:
            code = request.data.get('code')
            organization = Organization.objects.get(code=code)
            if not organization.is_active:
                return Response({"error": "Organization is banned."}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = ProgramCreateSerializer(data=request.data)
            if serializer.is_valid():
                program = serializer.save(
                    created_by=request.user,
                    organization=organization
                )
                return Response(ProgramAdminSerializer(program).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Organization.DoesNotExist:
            return Response({"detail": "Organization not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @invite_organization_schema
    @action(detail=True, methods=['post'])
    def invite_organization(self, request, pk=None):
        try:
            code = request.data.get('code')
            organization = Organization.objects.get(code=code)
            program = self.get_object()
            if ProgramInvite.objects.filter(organization=organization, program=program, is_active=True).exists():
                return Response({"error": "Organization is already invited to this program."}, status=status.HTTP_400_BAD_REQUEST)
            invite = ProgramInvite.objects.create(
                organization=organization,
                program=program,
                invited_by=request.user
            )
            return Response(ProgramInviteSerializer(invite).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @subscribe_program_schema
    @action(detail=True, methods=['post'])
    def subscribe(self, request, pk=None):
        program = self.get_object()
        if not program.is_active:
            return Response({"error": "Program is already archived."}, status=status.HTTP_400_BAD_REQUEST)
        existing_subscription = ProgramSubscriber.objects.filter(
            program=program,
            subscriber=request.user
        ).first()

        if existing_subscription:
            if existing_subscription.is_active:
                return Response({"error": "Already subscribed to this program."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Reactivate the previous subscription
                existing_subscription.is_active = True
                existing_subscription.unsubscribed_at = None
                existing_subscription.subscribed_at = timezone.now()
                existing_subscription.save()
                return Response({"message": "Subscription reactivated successfully."}, status=status.HTTP_200_OK)
    
        ProgramSubscriber.objects.create(
            program=program,
            subscriber=request.user,
            subscribed_at=timezone.now()
        )
        return Response({"message": "Successfully subscribed to the program."}, status=status.HTTP_201_CREATED)
        
    @unsubscribe_program_schema
    @action(detail=True, methods=['post'])
    def unsubscribe(self, request, pk=None):
        program = self.get_object()
        if not program.is_active:
            return Response({"error": "Program is already archived."}, status=status.HTTP_400_BAD_REQUEST)

        subscription = ProgramSubscriber.objects.filter(
            program=program,
            subscriber=request.user,
            is_active=True
        ).first()

        if not subscription:
            return Response({"error": "You are not subscribed to this program."}, status=status.HTTP_400_BAD_REQUEST)

        subscription.is_active = False
        subscription.unsubscribed_at = timezone.now()
        subscription.save()

        return Response({"message": "Successfully unsubscribed from the program."}, status=status.HTTP_200_OK)
        
    @my_subscribed_programs_schema
    @action(detail=False, methods=['get'])
    def my_subscribed_programs(self, request, *args, **kwargs):
        subscriptions = ProgramSubscriber.objects.filter(subscriber=request.user, is_active=True).select_related('program', 'program__organization')
        paginated_queryset = self.paginate_queryset(subscriptions)
        if paginated_queryset is not None:
            serializer = ProgramSubscriberGetProgsSerializer(paginated_queryset, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ProgramSubscriberGetProgsSerializer(subscriptions, many=True)
        return Response(serializer.data)

    @archive_program_schema
    @action(detail=True, methods=['post'])
    def archive_program(self, request, pk=None):
        program = self.get_object()
        if not program.is_active:
            return Response({"error": "Program is already archived."}, status=status.HTTP_400_BAD_REQUEST)
        program.is_active = False
        program.archived_by = request.user
        program.archived_at = timezone.now()
        program.save()
        return Response(ProgramSerializer(program).data, status=status.HTTP_200_OK)

    
    @assign_program_event_admin_schema
    @action(detail=True, methods=['post'])
    def assign_program_event_admin(self, request, pk=None):
        program = self.get_object()
        if not program.is_active:
            return Response({"error": "Program is archived."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = AssignProgramEventAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data
        try:
            email = request.data.get('email')
            assigned_user = User.objects.get(email=email)
            if not assigned_user.is_active:
                return Response({"error": "User is banned."}, status=status.HTTP_400_BAD_REQUEST)
            
            if ProgramEventAdmin.objects.filter(user=assigned_user, program=program).exists():
                if not ProgramEventAdmin.objects.filter(user=assigned_user, program=program).first().is_active:
                    return Response({"error": "User has been revoked as program admin."}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"error": "User is already assigned as program admin."}, status=status.HTTP_400_BAD_REQUEST)

            prog_admin = ProgramEventAdmin.objects.create(
                program=program,
                user=assigned_user,
                role=validated['role'],
                can_add_another_admin=validated['can_add_another_admin'],
                can_archive_program=validated['can_archive_program'],
                can_archive_event=validated['can_archive_event'],
                can_add_event_organizer=validated['can_add_event_organizer'],
                can_remove_event_organizer_from_program=validated['can_remove_event_organizer_from_program'],
                can_change_attendance_validity=validated['can_change_attendance_validity'],
                can_create_events=validated['can_create_events'],
                can_conclude_events=validated['can_conclude_events'],
                added_by=request.user
            )
            
            return Response(ProgramEventAdmin_AdminSerializer(prog_admin).data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @revoke_program_event_admin_schema
    @action(detail=True, methods=['post'])
    def revoke_program_event_admin(self, request, pk=None):
        program = self.get_object()
        if not program.is_active:
            return Response({"error": "Program is archived."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = AssignProgramEventAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data
        try:
            email = request.data.get('email')
            assigned_user = User.objects.get(email=email)
            if not assigned_user.is_active:
                return Response({"error": "User is banned."}, status=status.HTTP_400_BAD_REQUEST)
            
            prog_admin = ProgramEventAdmin.objects.get(user=assigned_user, program=program)
            if not prog_admin.is_active:
                return Response({"error": "User has already been revoked as program admin."}, status=status.HTTP_400_BAD_REQUEST)

            prog_admin.is_active = False
            prog_admin.removed_by = request.user
            prog_admin.removed_at = timezone.now()
            prog_admin.save()
            return Response(ProgramEventAdmin_AdminSerializer(prog_admin).data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except ProgramEventAdmin.DoesNotExist:
            return Response({"detail": "Program admin not assigned."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @update_program_event_admin_schema
    @action(detail=True, methods=['patch'])
    def update_program_event_admin(self, request, pk=None):
        program = self.get_object()
        if not program.is_active:
            return Response({"error": "Program is archived."}, status=status.HTTP_400_BAD_REQUEST)

        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required to identify the admin."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                return Response({"error": "User is banned."}, status=status.HTTP_400_BAD_REQUEST)

            prog_admin = ProgramEventAdmin.objects.get(user=user, program=program)
            if not prog_admin.is_active:
                return Response({"error": "User has been revoked as program admin."}, status=status.HTTP_400_BAD_REQUEST)

            serializer = PatchProgramEventAdminSerializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            for attr, value in serializer.validated_data.items():
                setattr(prog_admin, attr, value)

            prog_admin.save()
            return Response(ProgramEventAdmin_AdminSerializer(prog_admin).data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except ProgramEventAdmin.DoesNotExist:
            return Response({"detail": "Program admin not assigned."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @get_all_program_event_admins_schema
    @action(detail=True, methods=['get'])
    def get_all_program_event_admins(self, request, *args, **kwargs):
        program = self.get_object()
        if not program.is_active:
            return Response({"error": "Program is archived."}, status=status.HTTP_400_BAD_REQUEST)
        program_admins = ProgramEventAdmin.objects.filter(program=program).select_related(
            'user', 'added_by', 'removed_by', 'program', 'program__organization'
        )
        paginated_queryset = self.paginate_queryset(program_admins)
        if paginated_queryset is not None:
            serializer = ProgramEventAdmin_AdminSerializer(paginated_queryset, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ProgramEventAdmin_AdminSerializer(program_admins, many=True)
        return Response(serializer.data)
    
    @get_user_program_event_admins_schema
    @action(detail=True, methods=['get'])
    def get_user_program_event_admins(self, request, *args, **kwargs):
        try:
            email = request.query_params.get('email')
            user = User.objects.get(email=email)
            program = self.get_object()
            if not program.is_active:
                return Response({"error": "Program is archived."}, status=status.HTTP_400_BAD_REQUEST)
        
            program_admin = ProgramEventAdmin.objects.get(program=program, user=user)
            serializer = ProgramEventAdmin_AdminSerializer(program_admin)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except ProgramEventAdmin.DoesNotExist:
            return Response({"detail": "User is not assigned as program admin in this organization."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class NestedSubscribersViewset(ListModelMixin, GenericViewSet):
    queryset = ProgramSubscriber.objects.none()
    serializer_class = ProgramSubscriberGetSubsSerializer
    permission_classes = [NestedSubscribersViewsetPermissions]
    pagination_class = CustomPageNumberPagination

    @list_subscribers_in_program_schema
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def get_queryset(self):
        program_id = self.kwargs.get('program_pk')
        return ProgramSubscriber.objects.filter(program__id=program_id, is_active=True).select_related('subscriber')


class NestedSubscribedProgramsViewset(ListModelMixin, GenericViewSet):
    queryset = ProgramSubscriber.objects.none()
    serializer_class = ProgramSubscriberGetProgsSerializer
    permission_classes = [NestedSubscribedProgramsViewsetPermissions]
    pagination_class = CustomPageNumberPagination

    @list_subscribed_programs_schema
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def get_queryset(self):
        subscriber_id = self.kwargs.get('subscriber_pk')
        return ProgramSubscriber.objects.filter(subscriber__id=subscriber_id, is_active=True).select_related('program', 'program__organization')


class NestedOrganizationProgramViewset(ListModelMixin, GenericViewSet):
    serializer_class = ProgramSerializer
    queryset = Program.objects.none()
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination

    @list_organization_programs_schema
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return ProgramAdminSerializer
        return ProgramListNestedSerializer
    
    def get_queryset(self):
        organization_id = self.kwargs.get('organization_pk')
        return Program.objects.filter(organization__id=organization_id).select_related('organization', 'created_by', 'archived_by')

    @list_organization_associated_programs_schema
    @action(detail=False, methods=['get'])
    def associated_programs(self, request, *args, **kwargs):
        try:
            organization_id = self.kwargs.get('organization_pk')
            organization = Organization.objects.get(id=organization_id)
            if not organization.is_active:
                return Response({"error": "Organization is banned."}, status=status.HTTP_400_BAD_REQUEST)
            programs = Program.objects.filter(invited_programs__organization=organization).select_related('organization', 'created_by', 'archived_by')
            print("ooo")
            paginated_queryset = self.paginate_queryset(programs)
            if paginated_queryset is not None:
                serializer = self.get_serializer(paginated_queryset, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(programs, many=True)
            return Response(serializer.data)
        except Organization.DoesNotExist:
            return Response({"error": "Organization not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ProgramInviteViewset(GenericViewSet):
    serializer_class = ProgramInviteSerializer
    queryset = ProgramInvite.objects.all()
    permission_classes = [ProgramInviteViewsetPermissions]
    pagination_class = CustomPageNumberPagination
    
    @undo_invite_organization_schema
    @action(detail=True, methods=['post'])
    def undo_invite_organization(self, request, pk=None):
        try:
            invite = self.get_object()
            if not invite.is_active:
                return Response({"error": "Invite is already undone."}, status=status.HTTP_400_BAD_REQUEST)
            if invite.removed_by:
                return Response({"error": "Invite is already removed."}, status=status.HTTP_400_BAD_REQUEST)
            invite.is_active = False
            invite.removed_by = request.user
            invite.removed_at = timezone.now()
            invite.save()
            invited_organization_program = InvitedOrganizationProgram.objects.filter(invite=invite)
            if invited_organization_program.exists():
                invited_organization_program.update(
                    is_active=False,
                    removed_by=request.user,
                    removed_at=timezone.now()
                )
            return Response(ProgramInviteSerializer(invite).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    @accept_invite_schema
    @action(detail=True, methods=['post'])
    def accept_invite(self, request, pk=None):
        try:
            invite = self.get_object()
            if not invite.is_active:
                return Response({"error": "Invite is undone."}, status=status.HTTP_400_BAD_REQUEST)
            if invite.accepted_by:
                return Response({"error": "Invite is already accepted."}, status=status.HTTP_400_BAD_REQUEST)
            if InvitedOrganizationProgram.objects.filter(program=invite.program, is_active=True).exists():
                return Response({"error": "Organization is already in this program."}, status=status.HTTP_400_BAD_REQUEST)
            invite.accepted_by = request.user
            invite.accepted_at = timezone.now()
            invite.save()
            invited_organization_program = InvitedOrganizationProgram.objects.create(
                organization=invite.organization,
                program=invite.program,
                invite=invite,
                accepted_by=request.user,
                accepted_at=timezone.now()
            )
            return Response(ProgramInviteSerializer(invite).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @reject_invite_schema
    @action(detail=True, methods=['post'])
    def reject_invite(self, request, pk=None):
        try:
            invite = self.get_object()
            if not invite.is_active:
                return Response({"error": "Invite is undone."}, status=status.HTTP_400_BAD_REQUEST)
            if invite.rejected_by:
                return Response({"error": "Invite is already rejected."}, status=status.HTTP_400_BAD_REQUEST)
            invite.rejected_by = request.user
            invite.rejected_at = timezone.now()
            invite.save()
            invited_organization_program = InvitedOrganizationProgram.objects.filter(invite=invite)
            if invited_organization_program.exists():
                invited_organization_program.update(
                    is_active=False,
                    rejected_by=request.user,
                    rejected_at=timezone.now()
                )
            return Response(ProgramInviteSerializer(invite).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class NestedProgramInviteViewset(ListModelMixin, GenericViewSet):
    serializer_class = ProgramInviteSerializer
    queryset = ProgramInvite.objects.none()
    permission_classes = [NestedProgramInviteViewsetPermissions]
    pagination_class = CustomPageNumberPagination

    @list_program_invites_schema
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        program_id = self.kwargs.get('program_pk')
        return ProgramInvite.objects.filter(program__id=program_id).select_related(
            'program', 'program__organization',
            'organization',
            'invited_by', 'accepted_by', 'rejected_by', 'removed_by'
        )

    def get_serializer_class(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return ProgramInviteAdminSerializer
        return ProgramInviteSerializer
    

class NestedOrganizationInviteViewset(ListModelMixin, GenericViewSet):
    serializer_class = ProgramInviteSerializer
    queryset = ProgramInvite.objects.none()
    permission_classes = [NestedOrganizationInviteViewsetPermissions]
    pagination_class = CustomPageNumberPagination

    @list_organizations_invites_schema
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        organization_id = self.kwargs.get('organization_pk')
        return ProgramInvite.objects.filter(organization__id=organization_id).select_related(
            'program', 'program__organization',
            'organization',
            'invited_by', 'accepted_by', 'rejected_by', 'removed_by'
        )

    def get_serializer_class(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return ProgramInviteAdminSerializer
        return ProgramInviteSerializer
    

class ProgramInvitedOrganizationViewset(GenericViewSet):
    serializer_class = InvitedOrganizationProgramSerializer
    queryset = InvitedOrganizationProgram.objects.all()
    permission_classes = [ProgramInvitedOrganizationViewsetPermissions]
    pagination_class = CustomPageNumberPagination

    @leave_program_schema
    @action(detail=True, methods=['post'])
    def leave_program(self, request, pk=None):
        try:
            invited_organization_program = self.get_object()
            if invited_organization_program.removed_by:
                return Response({"error": "Had left the program already."}, status=status.HTTP_400_BAD_REQUEST)
            if not invited_organization_program.is_active:
                return Response({"error": "Invite is already undone."}, status=status.HTTP_400_BAD_REQUEST)
            invited_organization_program.is_active = False
            invited_organization_program.removed_by = request.user
            invited_organization_program.removed_at = timezone.now()
            invited_organization_program.save()
            return Response(InvitedOrganizationProgramSerializer(invited_organization_program).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class NestedOrganizationAssociatedProgramViewset(ListModelMixin, GenericViewSet):
    serializer_class = InvitedOrganizationProgramSerializer
    queryset = InvitedOrganizationProgram.objects.none()
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination

    @list_organization_invited_programs_schema
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return InvitedOrganizationProgramAdminSerializer
        return InvitedOrganizationProgramSerializer
    
    def get_queryset(self):
        organization_id = self.kwargs.get('organization_pk')
        return InvitedOrganizationProgram.objects.filter(organization__id=organization_id).select_related(
            'program', 'program__organization',
            'invite', 'invite__organization', 'invite__program', 'invite__program__organization',
            'accepted_by', 'organization'
        )

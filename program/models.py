from django.db import models
import uuid

# Create your models here.
class Program(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, related_name='programs')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    archived_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='created_programs')
    archived_by = models.ForeignKey('account.User', on_delete=models.CASCADE, null=True, blank=True, related_name='archived_programs')

    def __str__(self):
        return f"{self.name} by Organization: {self.organization.name}"


class ProgramInvite(models.Model):
    id = models.AutoField(primary_key=True)
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, related_name='invited_to_programs')
    program = models.ForeignKey('program.Program', on_delete=models.CASCADE, related_name='invited_organizations')
    is_active = models.BooleanField(default=True)
    invited_by = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='invites_sent')
    accepted_by = models.ForeignKey('account.User', on_delete=models.CASCADE, null=True, blank=True, related_name='accepted_invites')
    rejected_by = models.ForeignKey('account.User', on_delete=models.CASCADE, null=True, blank=True, related_name='rejected_invites')
    removed_by = models.ForeignKey('account.User', on_delete=models.CASCADE, null=True, blank=True, related_name='removed_invites')
    invited_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    rejected_at = models.DateTimeField(null=True, blank=True)
    removed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Organization: {self.organization.name} Invited to program {self.program.name} by {self.invited_by.name}"

class InvitedOrganizationProgram(models.Model):
    id = models.AutoField(primary_key=True)
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, related_name='invited_programs')
    program = models.ForeignKey('program.Program', on_delete=models.CASCADE, related_name='invited_programs')
    is_active = models.BooleanField(default=True)
    invite = models.ForeignKey('program.ProgramInvite', on_delete=models.CASCADE)
    accepted_by = models.ForeignKey('account.User', on_delete=models.CASCADE, null=True, blank=True, related_name='accepted_programs')
    rejected_by = models.ForeignKey('account.User', on_delete=models.CASCADE, null=True, blank=True, related_name='rejected_programs')
    removed_by = models.ForeignKey('account.User', on_delete=models.CASCADE, null=True, blank=True, related_name='removed_programs')
    accepted_at = models.DateTimeField(null=True, blank=True)
    rejected_at = models.DateTimeField(null=True, blank=True)
    removed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Organization: {self.organization.name} Invited to program {self.program.name} by {self.invite.invited_by.name}"

class ProgramSubscriber(models.Model):
    id = models.AutoField(primary_key=True)
    program = models.ForeignKey('program.Program', on_delete=models.CASCADE, related_name='subscribers')
    is_active = models.BooleanField(default=True)
    subscriber = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='subscribed_programs')
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"User: {self.subscriber.name} Subscribed to program {self.program.name} at {self.subscribed_at}"

class ProgramEventAdmin(models.Model):
    ROLE_DEFAULT = 'Admin'
    CAN_ADD_ANOTHER_ADMIN = False
    CAN_ARCHIVE_PROGRAM = False
    CAN_ARCHIVE_EVENT = False
    CAN_ADD_EVENT_ORGANIZER = True
    CAN_REMOVE_EVENT_ORGANIZER_FROM_PROGRAM = False
    CAN_CHANGE_ATTENDANCE_VALIDITY = False
    CAN_CHANGE_ATTENDANCE_VALIDITY = False
    CAN_CREATE_EVENTS = True
    CAN_CONCLUDE_EVENTS = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='event_admin_roles')
    program = models.ForeignKey('program.Program', on_delete=models.CASCADE, related_name='event_admins')
    role = models.CharField(max_length=100, default=ROLE_DEFAULT)
    is_active = models.BooleanField(default=True)
    is_program_super_admin = models.BooleanField(default=False)
    can_add_another_admin = models.BooleanField(default=CAN_ADD_ANOTHER_ADMIN)
    can_archive_program = models.BooleanField(default=CAN_ARCHIVE_PROGRAM)
    can_archive_event = models.BooleanField(default=CAN_ARCHIVE_EVENT)
    can_add_event_organizer = models.BooleanField(default=CAN_ADD_EVENT_ORGANIZER)
    can_remove_event_organizer_from_program = models.BooleanField(default=CAN_REMOVE_EVENT_ORGANIZER_FROM_PROGRAM)
    can_change_attendance_validity = models.BooleanField(default=CAN_CHANGE_ATTENDANCE_VALIDITY)
    can_create_events = models.BooleanField(default=CAN_CREATE_EVENTS)
    can_conclude_events = models.BooleanField(default=CAN_CONCLUDE_EVENTS)
    added_by = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='added_event_admins')
    removed_by = models.ForeignKey('account.User', on_delete=models.CASCADE, null=True, blank=True, related_name='removed_event_admins')
    added_at = models.DateTimeField(auto_now_add=True)
    removed_at = models.DateTimeField(null=True, blank=True)
    left_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"User: {self.user.name}, Event Admin of program {self.program.name}"

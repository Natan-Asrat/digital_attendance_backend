from django.db import models
import uuid

class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=512)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    archived_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        related_name="organizations_created"
    )
    archived_by = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="organizations_archived"
    )
    
    def __str__(self):
        return self.name

class OrganizationAdmin(models.Model):
    # used defaults in serializer too, trying to keep consistency
    ROLE_DEFAULT = 'Admin'
    CAN_ADD_ANOTHER_ADMIN = False
    CAN_ARCHIVE_ORGANIZATION = False
    CAN_CHANGE_ATTENDANCE_VALIDITY = False
    CAN_CREATE_PROGRAMS = False

    id = models.IntegerField(primary_key=True)  # if you want a manual ID
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='organization_admin_roles')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='organization_admins')
    role = models.CharField(max_length=100, default=ROLE_DEFAULT)
    is_active = models.BooleanField(default=True)
    is_organization_super_admin = models.BooleanField(default=False)
    can_add_another_admin = models.BooleanField(default=CAN_ADD_ANOTHER_ADMIN)
    can_archive_organization = models.BooleanField(default=CAN_ARCHIVE_ORGANIZATION)
    can_change_attendance_validity = models.BooleanField(default=CAN_CHANGE_ATTENDANCE_VALIDITY)
    can_create_programs = models.BooleanField(default=CAN_CREATE_PROGRAMS)
    added_by = models.ForeignKey(
        'account.User', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='organization_admins_added'
    )
    removed_by = models.ForeignKey(
        'account.User', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='organization_admins_removed'
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)
    removed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.organization} ({'Super Admin' if self.is_organization_super_admin else self.role})"

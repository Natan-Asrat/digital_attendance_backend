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

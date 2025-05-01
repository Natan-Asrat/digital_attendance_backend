from django.db import models
import uuid
import string
import random

# Create your models here.
class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=255)
    description = models.TextField()
    short_code = models.CharField(max_length=8, unique=True, editable=False)
    program = models.ForeignKey('program.Program', on_delete=models.CASCADE)
    is_archived = models.BooleanField(default=False)
    is_concluded = models.BooleanField(default=False)
    # public_event = models.BooleanField(default=False) next versions with invite based private events
    created_by = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='created_events')
    archived_by = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='archived_events', null=True, blank=True)
    concluded_by = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='concluded_events', null=True, blank=True)
    reactivated_by = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='reactivated_events', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    archived_at = models.DateTimeField(null=True, blank=True)
    concluded_at = models.DateTimeField(null=True, blank=True)
    reactivated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} by Program: {self.program.name}"

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = self._generate_unique_short_code()
        return super().save(*args, **kwargs)

    def _generate_unique_short_code(self):
        chars = string.ascii_lowercase
        while True:
            code = ''.join(random.choices(chars, k=8))
            if not Event.objects.filter(short_code=code).exists():
                return code

class Attendance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    event = models.ForeignKey('event.Event', on_delete=models.CASCADE)
    attendee = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='attended_events')
    display_name = models.CharField(max_length=255, null=True, blank=True)
    valid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    validated_at = models.DateTimeField(null=True, blank=True)
    invalidated_at = models.DateTimeField(null=True, blank=True)
    validated_by = models.ForeignKey('account.User', on_delete=models.CASCADE, null=True, blank=True, related_name='validated_attendances')
    invalidated_by = models.ForeignKey('account.User', on_delete=models.CASCADE, null=True, blank=True, related_name='invalidated_attendances')

    def __str__(self):
        return f"{self.attendee.name} Attendance for Event: {self.event.title}, Program: {self.event.program.name}"

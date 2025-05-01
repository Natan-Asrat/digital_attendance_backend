from django.contrib import admin
from .models import Program, ProgramInvite, InvitedOrganizationProgram

# Register your models here.
admin.site.register(Program)
admin.site.register(ProgramInvite)
admin.site.register(InvitedOrganizationProgram)

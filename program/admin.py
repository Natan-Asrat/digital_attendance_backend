from django.contrib import admin
from .models import Program, ProgramInvite, InvitedOrganizationProgram, ProgramSubscriber, ProgramEventAdmin

# Register your models here.
admin.site.register(Program)
admin.site.register(ProgramInvite)
admin.site.register(InvitedOrganizationProgram)
admin.site.register(ProgramSubscriber)
admin.site.register(ProgramEventAdmin)
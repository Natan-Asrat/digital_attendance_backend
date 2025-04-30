from django.contrib import admin
from .models import Organization, OrganizationAdmin

# Register your models here.
admin.site.register(Organization)
admin.site.register(OrganizationAdmin)
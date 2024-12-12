from django.contrib import admin
from . import models

class DisciplinaryIncidentAdmin(admin.ModelAdmin):
    list_display = ("incident_id", "student", "description","date","severity_level","reported_by")

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "bio")

admin.site.register(models.DisciplinaryIncident, DisciplinaryIncidentAdmin)
admin.site.register(models.Profile, ProfileAdmin)





from django.contrib import admin
from . import models

class DisciplinaryIncidentAdmin(admin.ModelAdmin):
    list_display = ("incident_id", "student", "description","date","severity_level","reported_by")

admin.site.register(models.DisciplinaryIncident, DisciplinaryIncidentAdmin)





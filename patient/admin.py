from django.contrib import admin

from patient.models import Patient #patient is the application name

# Register your models here.
admin.site.register(Patient)
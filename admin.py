from django.contrib import admin
from . import models

class PresentationInline(admin.TabularInline):
    model = models.Presentation

class ProgramAdmin(admin.ModelAdmin):
    inlines = [
        PresentationInline,
    ]
# Register your models here.
admin.site.register(models.Program, ProgramAdmin)
admin.site.register(models.Presentation)

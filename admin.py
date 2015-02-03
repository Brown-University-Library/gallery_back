from django.contrib import admin
from . import models

class SlideInline(admin.TabularInline):
    model = models.Slide

class ProgramAdmin(admin.ModelAdmin):
    inlines = [
        SlideInline,
    ]
# Register your models here.
admin.site.register(models.Program, ProgramAdmin)
admin.site.register(models.Slide)

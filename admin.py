from django.contrib import admin
from . import models

class SlideInline(admin.TabularInline):
    model = models.Slide

class PresentationAdmin(admin.ModelAdmin):
    inlines = [
        SlideInline,
    ]
# Register your models here.
admin.site.register(models.Presentation, PresentationAdmin)

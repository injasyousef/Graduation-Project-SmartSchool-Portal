from django.contrib import admin

from common.models import City, ParentJob, Religion

# Register your models here.
admin.site.register(City)
admin.site.register(ParentJob)
admin.site.register(Religion)
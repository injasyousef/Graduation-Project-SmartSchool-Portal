from django.contrib import admin

from health_and_behavioral.models import HealthRecord, BehaviourEvaluation

# Register your models here.
admin.site.register(HealthRecord)
admin.site.register(BehaviourEvaluation)

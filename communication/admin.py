from django.contrib import admin

from communication.models import Message, Advertisement

# Register your models here.
admin.site.register(Advertisement)
admin.site.register(Message)
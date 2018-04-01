from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'time')
    ordering = ('-time',)

# Register your models here.
admin.site.register(Message, MessageAdmin)
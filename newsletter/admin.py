from django.contrib import admin
from .models import Subscriber, Newsletter

class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'time_added', 'uuid')
    ordering = ('-time_added',)
    list_filter = ('time_added',)

# Register your models here.
admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Newsletter)
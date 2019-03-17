from django.contrib import admin
from newsletter.models import Subsr

class SubsrAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'date_joined')

# Register your models here.
admin.site.register(Subsr, SubsrAdmin)

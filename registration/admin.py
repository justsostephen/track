from django.contrib import admin
from registration.models import Delegate

class DelegateAdmin(admin.ModelAdmin):
    list_display = ['delegate', 'item', 'accessory', 'status',
        'timestamp_issue', 'timestamp_return']
    list_filter = ['status', 'timestamp_issue', 'timestamp_return', 'accessory']
    search_fields = ['delegate', 'item']

admin.site.register(Delegate, DelegateAdmin)

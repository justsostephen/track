from django.contrib import admin
from lending.models import User, Item, Tablet, BugsFeatures

class UserAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'barcode']
    list_filter = ['name']
    search_fields = ['name', 'barcode']

class BugsFeaturesAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'bug_feature', 'status']
    list_filter = ['user', 'status']
    search_fields = ['id', 'user__name', 'status']

admin.site.register(User, UserAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Tablet, ItemAdmin)
admin.site.register(BugsFeatures, BugsFeaturesAdmin)

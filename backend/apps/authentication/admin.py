from django.contrib import admin
from apps.authentication.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'first_name', 'last_name',
                    'email', 'is_staff', 'is_active')
    search_fields = ('phone_number', 'first_name', 'last_name', 'email')
    readonly_fields = ('date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, UserAdmin)

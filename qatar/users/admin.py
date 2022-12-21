from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

# Register your models here.
@admin.register(get_user_model())
class CustomUSerAdmin(UserAdmin):
    list_display = (
        'username', 'is_superuser',
        'is_active', 'is_site_admin',
        'is_manager'
    )
    list_filter = (
        'is_superuser', 'is_active',
        'is_site_admin', 'is_manager'
    )
    search_fields = ('username',)
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': (
            'username', 
            'password'
        )}),
        (_('Personal info'), {'fields': (
            'first_name',
            'last_name',
            'email',
            'gender',
            'birthday',
            'nationality',
        )}),
        (_('Permissions'), {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'is_site_admin',
            'is_manager',
            'groups',
            'user_permissions',
        )}),
        (_('Important dates'), {'fields': (
            'last_login', 
            'date_joined'
        )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'gender',
                'birthday',
                'nationality',
                'email',
                'is_active',
                'is_staff',
                'is_superuser',
                'is_site_admin',
                'is_manager',
                'groups',
                'user_permissions',
            )}
        ),
    )
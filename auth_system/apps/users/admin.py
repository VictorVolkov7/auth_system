from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Role, BusinessElement, AccessRoleRule, Session


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin panel for User model."""
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """Admin panel for Role model."""
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(BusinessElement)
class BusinessElementAdmin(admin.ModelAdmin):
    """Admin panel for BusinessElement model."""
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(AccessRoleRule)
class AccessRoleRuleAdmin(admin.ModelAdmin):
    """Admin panel for AccessRoleRule model."""
    list_display = ('role', 'element', 'read_permission', 'read_all_permission', 'create_permission',
                    'update_permission', 'update_all_permission', 'delete_permission', 'delete_all_permission')
    list_filter = ('role', 'element')
    search_fields = ('role__name', 'element__name')
    ordering = ('role__name', 'element__name')


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    """Admin panel for Session model."""
    list_display = ('user', 'session_key', 'expire_at', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('user__email', 'session_key')
    ordering = ('-expire_at',)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import Account, Person

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("user_id", "email", "created_at")
    search_fields = ("user_id", "email")

@admin.register(Account)
class AccountAdmin(DjangoUserAdmin):
    model = Account
    list_display = ("email", "role", "is_active", "is_staff", "user_id")
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("email",)
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password", "user_id")}),
        ("Permissions", {"fields": ("role", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Dates", {"fields": ("last_login", "created_at", "last_login_at")}),
    )
    readonly_fields = ("created_at", "last_login_at", "user_id")
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2", "role")}),
    )

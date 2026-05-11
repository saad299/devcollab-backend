from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile

# Register your models here.
# admin.site.register(User, UserAdmin)

class ProfileInline(admin.TabularInline):
    model = Profile
    fields = ['bio', 'skills', 'location', 'github_url']
    can_delete = False
    extra = 0

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]
    list_display = ['username', 'email', 'date_joined', 'is_staff']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['username', 'email']
    ordering = ['-date_joined']

    # fieldsets = UserAdmin.fieldsets + (
    #     ('Email Verification', {
    #         'fields': ('email_verified',)
    #     }),
    # )
    # fieldsets = (
    #     *UserAdmin.fieldsets,
    #     (
    #         'Email Verification',
    #         {
    #             'fields': ('email_verified',)
    #         }
    #     ),
    # )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'github_url']
    search_fields = ['user__username', 'user__email', 'skills']
    list_filter = ['location']
from django.contrib import admin
from .models import CustomUser, OTP, Report
from django.contrib.auth.admin import UserAdmin

def approve_users(modeladmin, request, queryset):
    updated = queryset.update(admin_verified=True, is_active=True, status='approved')
    modeladmin.message_user(request, f"{updated} user(s) approved.")
approve_users.short_description = "Approve selected users"

def reject_users(modeladmin, request, queryset):
    updated = queryset.update(status='rejected', is_active=False)
    modeladmin.message_user(request, f"{updated} user(s) rejected.")
reject_users.short_description = "Reject selected users"

def block_users(modeladmin, request, queryset):
    updated = queryset.update(is_blocked=True, status='blocked')
    modeladmin.message_user(request, f"{updated} user(s) blocked.")
block_users.short_description = "Block selected users"

def unblock_users(modeladmin, request, queryset):
    updated = queryset.update(is_blocked=False)
    modeladmin.message_user(request, f"{updated} user(s) unblocked.")
unblock_users.short_description = "Unblock selected users"

def approve_address(modeladmin, request, queryset):
    count = 0
    for user in queryset:
        if user.pending_address:
            user.address = user.pending_address
            user.pending_address = ""
            user.save()
            count += 1
    modeladmin.message_user(request, f"{count} address(es) approved.")
approve_address.short_description = "Approve pending addresses"

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'registration_number', 'email', 'phone', 'status', 'admin_verified', 'is_blocked', 'email_verified', 'phone_verified', 'created_at']
    list_filter = ['status', 'admin_verified', 'is_blocked', 'email_verified', 'phone_verified', 'created_at']
    search_fields = ['username', 'email', 'phone', 'registration_number']
    actions = [approve_users, reject_users, block_users, unblock_users, approve_address]
    fieldsets = UserAdmin.fieldsets + (
        ('Extra', {'fields': ('registration_number','status','phone','address','pending_address','email_verified','phone_verified','admin_verified','is_blocked','created_at')}),
    )
    readonly_fields = ['registration_number', 'created_at']

class ReportAdmin(admin.ModelAdmin):
    list_display = ['user','report_date','amount','bank_number','ifsc_code','status','created_at']
    list_filter = ['status','report_date','created_at']
    search_fields = ['user__username','bank_number','ifsc_code']
    readonly_fields = ['created_at','updated_at']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OTP)
admin.site.register(Report, ReportAdmin)
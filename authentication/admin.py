from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.utils.html import format_html

class StudentDetailsInline(admin.StackedInline):
    model = StudentDetails
    extra = 0

class AlumniDetailsInline(admin.StackedInline):
    model = AlumniDetails
    extra = 0


class WorkingProfessionalInline(admin.StackedInline):
    model = WorkingProfessional
    extra = 0

class HigherStudiesInline(admin.StackedInline):
    model = HigherStudies
    extra = 0

class StartupInlie(admin.StackedInline):
    model = Startup
    extra = 0

class OthersInline(admin.StackedInline):
    model = Others
    extra = 0


# --- Custom User Admin ---
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("profile_pic_preview","id", "username", "email", "first_name", "last_name","course_name", "role")

    # while editing
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("role", "roll_no", "enrolment_no", "starting_year", "ending_year", "course_name", "profile_pic")}),
    )

    # while creating
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("profile_pic", "role", "roll_no", "enrolment_no", "starting_year", "ending_year", "course_name")}),
    )
    
    def profile_pic_preview(self, obj):
        if obj.profile_pic:
            return format_html('<img src="{}" width="40" height="40" style="border-radius:50%;" />', obj.profile_pic.url)
        return "No Image"


    def get_inlines(self, request, obj=None):
        """Show StudentDetailsInline only for Students, AlumniDetailsInline only for Alumni."""
        if obj:  # Editing an existing user
            if obj.role == "Student":
                return [StudentDetailsInline]
            elif obj.role == "Alumni":
                return [AlumniDetailsInline]
        return []  # When adding a new user, don’t show any inlines yet


# AlumniDetails Admin (for subcategories) 
class AlumniDetailsAdmin(admin.ModelAdmin):
    list_display = ("alumni", "current_status", "location")

    def get_inlines(self, request, obj=None):
        if obj:  # Only show after an alumni exists
            if obj.current_status == "Job":
                return [WorkingProfessionalInline]
            elif obj.current_status == "Higher Studies":
                return [HigherStudiesInline]
            elif obj.current_status == "Startup":
                return [StartupInlie]
            elif obj.current_status == "Other":
                return [OthersInline]
        return []


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(AlumniDetails, AlumniDetailsAdmin)
admin.site.register(StudentDetails)
admin.site.register(ManualVerification)
admin.site.register(WorkingProfessional)
admin.site.register(HigherStudies)
admin.site.register(Startup)
admin.site.register(Others)

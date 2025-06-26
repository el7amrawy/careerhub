from django.contrib import admin
from .models import Job, Category, Apply, Skill, SavedJob

class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'job_type', 'job_level', 'location', 'is_featured', 'is_active')
    list_filter = ('job_type', 'job_level', 'category', 'is_featured', 'is_active')
    search_fields = ('title', 'company_name', 'description')
    list_editable = ('is_featured', 'is_active')
    prepopulated_fields = {'slug': ('title',)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

class ApplyAdmin(admin.ModelAdmin):
    list_display = ('name', 'job', 'email', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'job__title')
    list_editable = ('status',)

class SavedJobAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'saved_at')
    list_filter = ('saved_at',)
    search_fields = ('user__username', 'job__title')

admin.site.register(Job, JobAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Apply, ApplyAdmin)
admin.site.register(SavedJob, SavedJobAdmin)
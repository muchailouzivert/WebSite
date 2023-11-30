from django.contrib.auth.models import Group, Permission, User
from django.contrib import admin
from .models import *


# Register your models here.

class AppUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')


admin.site.register(AppUser, AppUserAdmin)


class VacancyAdmin(admin.ModelAdmin):
    list_display = ('employer', 'job_type', 'salary', 'status')
    list_filter = ('status',)
    search_fields = ('employer__name', 'job_type')


admin.site.register(Vacancy, VacancyAdmin)


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'vacancy', 'submission_date', 'status')
    list_filter = ('status',)
    search_fields = ('user__name', 'vacancy__job_type')


admin.site.register(Application, ApplicationAdmin)

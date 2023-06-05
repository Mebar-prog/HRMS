from django.contrib import admin
from api.models import Employee

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'employee_id', 'gender', 'dob', 'designation', 'appointment_date')
    list_filter = ('gender',)
    search_fields = ('name', 'employee_id', 'designation')

admin.site.register(Employee, EmployeeAdmin)

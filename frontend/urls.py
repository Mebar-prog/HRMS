from django.contrib import admin
from django.urls import path
from frontend.views import *

app_name = 'frontend'

urlpatterns = [
    path('',index,name='index'),
    path('login',login,name='login'),
    path('logout',logout,name='logout'),
    path('dashboard',dashboard,name='dashboard'),
    path('employee',employee,name='employee'),
    path('employee/<int:employee_id>/', EmployeeDetail, name='EmployeeDetail'),
    path('edit_employee/<int:employee_id>/', edit_employee, name='edit_employee'),
    path('delete_employee/<int:employee_id>/', delete_employee, name='delete_employee'),
    path('employee/search/', search_employee, name='search_employee'),
    path('employee/filter/', filter_employee_by_date, name='filter_employee_by_date'),
    path('employee/sort/', sort_employee_by_gender, name='sort_employee_by_gender'),
    path('register/', register_employee, name='register_employee'),
    path('success/', success, name='success'),
    path('error/', error, name='error'),





]
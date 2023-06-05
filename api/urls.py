from django.urls import path
from .views import UserLoginAPIView,EmployeeListView,EmployeeDetailView,EmployeeDeleteAPIView,EmployeeSearchAPIView,EmployeeFilterAPIView,EmployeeSortAPIView,RegisterEmployeeAPIView

app_name="api"

urlpatterns = [
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('employees/', EmployeeListView.as_view(), name='employee_list'),
    path('employees/<int:employee_id>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('employees/<int:employee_id>/delete/', EmployeeDeleteAPIView.as_view(), name='employee_delete'),
    path('employees/search/', EmployeeSearchAPIView.as_view(), name='search_employees'),
    path('employees/filter/', EmployeeFilterAPIView.as_view(), name='employee_filter'),
    path('employees/sort/', EmployeeSortAPIView.as_view(), name='sort_employees'),
    path('employees/register/', RegisterEmployeeAPIView.as_view(), name='register_employee'),
    




]

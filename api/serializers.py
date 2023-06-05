from rest_framework import serializers

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


#employee serializers
from rest_framework import serializers
from api.models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['name', 'employee_id', 'gender', 'dob', 'designation', 'department', 'appointment_date']
        # read_only_fields = ['employee_id']


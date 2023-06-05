from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from rest_framework import status
from django.db.models import Q
from api.models import Employee
from api.serializers import EmployeeSerializer

#login
class UserLoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            access_token = AccessToken.for_user(user)
            return Response({'access_token': str(access_token)})
        else:
            return Response({'message': 'Invalid credentials'}, status=401)



#employee view:
class EmployeeListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)


#employee update, and get view 
class EmployeeDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get_object(self, employee_id):
        try:
            return Employee.objects.get(employee_id=employee_id)
        except Employee.DoesNotExist:
            raise Http404

    def get(self, request, employee_id):
        employee = self.get_object(employee_id)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
    
    def put(self, request, employee_id):
        employee = self.get_object(employee_id)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#delet employee

class EmployeeDeleteAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def delete(self, request, employee_id):
        # Retrieve the employee instance based on the provided employee_id
        employee = Employee.objects.get(employee_id=employee_id)
        # Delete the employee instance
        employee.delete()
        # Return a success response
        return Response({"message": "Employee deleted successfully"})


#search employee view


class EmployeeSearchAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        query = request.GET.get('query')
        employees = Employee.objects.filter(name__icontains=query)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#filter employee by appoinment date


class EmployeeFilterAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        appointment_date = request.GET.get('appointment_date')

        # Filter employees based on the appointment date
        employees = Employee.objects.filter(appointment_date=appointment_date)
        serializer = EmployeeSerializer(employees, many=True)

        return Response(serializer.data)


#sort by gender api view


class EmployeeSortAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        gender = request.GET.get('gender')

        # Filter employees based on gender
        employees = Employee.objects.filter(gender=gender)

        # Sort employees by name
        employees = employees.order_by('name')

        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)


#Employee Registration api view


class RegisterEmployeeAPIView(APIView):
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request):
        return Response("Method not allowed", status=405)

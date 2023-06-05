from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from django.conf import settings
import jwt
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from api.models import Employee

def is_valid_token(token):
    # Return True if the token is valid
    try:
        # using `PyJWT` library to decode the token for checking 
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        return True
    except jwt.ExpiredSignatureError:
        # Token has expired
        return False
    except jwt.InvalidTokenError:
        # Token is invalid
        return False

# Create your views here.
def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Make a POST request to the login API endpoint
        login_url = 'http://127.0.0.1:8000/api/login/'
        data = {'username': username, 'password': password}
        response = requests.post(login_url, data=data)

        if response.status_code == 200:
            try:
                # Extract the access token from the JSON response
                json_response = response.json()
                # print(json_response)
                token = json_response.get('access_token')

                request.session['access_token'] = token
                # print(token)
                if token:
                    # Stores the token in session for subsequent requests
                    return redirect('frontend:dashboard')
                else:
                    # Handle the case when the 'access' key is missing or has an unexpected value
                    return HttpResponse('Invalid API response')
            except ValueError:
                # Handle the case when the response is not valid JSON
                return HttpResponse('Invalid API response')
        else:
            # Handle the case when the login request returns a non 200 status code
            return HttpResponse('Login failed')
    else:
        # Render the login template
        return render(request, 'login.html')

def logout(request):
    # Clear the access token from the session
    if 'access_token' in request.session:
        del request.session['access_token']
    return redirect('frontend:login')


def dashboard(request):
    if 'access_token' not in request.session or not is_valid_token(request.session['access_token']):
        # Redirect the user to the login page if the token is not present or invalid
        return redirect('frontend:login')
    else:
        # Token is valid, proceed to fetch and display employee data
        access_token = request.session['access_token']
        api_url = 'http://127.0.0.1:8000/api/employees/'  # Replace with your API endpoint URL
        
        headers = {
            'Authorization': f'Bearer {access_token}',
        }
        
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200:
            employees = response.json()
            
            # Sort the employees by the creation date in descending order
            sorted_employees = sorted(employees, key=lambda x: x['appointment_date'], reverse=True)

            # Get only the first 5 employees
            recent_employees = sorted_employees[:5]

             # Calculate the total count of employees
            total_employees = len(employees)
            
            # Create a context dictionary with the employee data to be passed to the template
            context = {
                'recent_employees': recent_employees,
                'total_employees': total_employees,
            }
            
            # Render the template with the context data
            return render(request, 'dashboard.html', context)
        else:
            # Handle the case when the API request returns a non-200 status code
            return HttpResponse('Failed to fetch employee data')

#employee view with pagination


def employee(request):
    if 'access_token' not in request.session or not is_valid_token(request.session['access_token']):
        # Redirect the user to the login page if the token is not present or invalid
        return redirect('frontend:login')
    else:
        # Token is valid, proceed to fetch and pass employee data
        access_token = request.session['access_token']
        api_url = 'http://127.0.0.1:8000/api/employees/' 
        
        headers = {
            'Authorization': f'Bearer {access_token}',
        }
        
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200:
            employees = response.json()
            # Sort the employees by the creation date in descending order
            sorted_employees = sorted(employees, key=lambda x: x['appointment_date'], reverse=True)

            # Initialize the Paginator with the sorted employees and number of items per page
            paginator = Paginator(sorted_employees, 5)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {
                'recent_employees': page_obj,
                'page_obj': page_obj,
            }
            
            # Render the template with the context data
            return render(request, 'employee.html', context)
        else:
            # Handle the case when the API request returns a non-200 status code
            return HttpResponse('Failed to fetch employee data')



def EmployeeDetail(request, employee_id):
    if 'access_token' not in request.session or not is_valid_token(request.session['access_token']):
        # Redirect the user to the login page if the token is not present or invalid
        return redirect('frontend:login')
    else:
        # Retrieve the employee details based on the provided ID
        employee = get_object_or_404(Employee, pk=employee_id)
        
        # Pass the employee details to the template
        context = {
            'employee': employee,
        }
        
        # Render the template with the context data
        return render(request, 'e_details.html', context)







def edit_employee(request, employee_id):
    if 'access_token' not in request.session or not is_valid_token(request.session['access_token']):
        # Redirect the user to the login page if the token is not present or invalid
        return redirect('frontend:login')

    # Retrieve the employee details based on the provided ID
    employee = get_object_or_404(Employee, pk=employee_id)

    if request.method == 'POST':
        # Extract the updated employee details from the form data
        name = request.POST.get('name')
        gender = request.POST.get('gender') 
        dob = request.POST.get('dob')
        designation = request.POST.get('designation')
        department = request.POST.get('department')
        appointment_date = request.POST.get('appointment_date')

        print(f"name: {name}")
        print(f"employee_id: {employee_id}")
        print(f"gender: {gender}")
        print(f"dob: {dob}")
        print(f"designation: {designation}")
        print(f"department: {department}")
        print(f"appointment_date: {appointment_date}")

        # Make a PUT request to the API endpoint to update the employee details
        api_url = f'http://127.0.0.1:8000/api/employees/{employee_id}/'
        access_token = request.session['access_token']
        headers = {
            'Authorization': f'Bearer {access_token}',
        }
        data = {
            'name': name,
            'employee_id':employee_id,
            'gender': gender,
            'dob': dob,
            'designation': designation,
            'department': department,
            'appointment_date': appointment_date
        }

        response = requests.put(api_url, headers=headers, data=data)
        print("response content")
        print(response.content)  # Print the response content as raw bytes
        print("response.json")
        print(response.json())  # Print the response content as JSON

        if response.status_code == 200:
            # Employee details updated successfully
            return redirect('frontend:EmployeeDetail', employee_id=employee.employee_id)
        else:
            # Handle the case when the API request returns a non-200 status code
            print(response.content)
            return HttpResponse('Failed to update employee details')

    # Pass the employee details to the template for rendering the form
    context = {
        'employee': employee,
    }

    return render(request, 'e_details.html',context)



#employee delete view:import requests

def delete_employee(request, employee_id):
    if 'access_token' not in request.session or not is_valid_token(request.session['access_token']):
        # Redirect the user to the login page if the token is not present or invalid
        return redirect('frontend:login')

    # Make a DELETE request to the API endpoint to delete the employee
    api_url = f'http://127.0.0.1:8000/api/employees/{employee_id}/delete/'
    access_token = request.session['access_token']
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    response = requests.delete(api_url, headers=headers)

    if response.status_code == 200:
        # Employee deleted successfully
        return redirect('frontend:employee')
    else:
        # Handle the case when the API request returns a non-204 status code
        return HttpResponse('Failed to delete employee')



#search api

def search_employee(request):
    if request.method == 'GET':
        search_query = request.GET.get('query')

        # Make an API request to search employees based on the query
        api_url = f'http://127.0.0.1:8000/api/employees/search/?query={search_query}'
        access_token = request.session['access_token']
        headers = {
            'Authorization': f'Bearer {access_token}',
        }

        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            search_results = response.json()
        else:
            search_results = []

        context = {
            'recent_employees': search_results,
        }
        return render(request, 'employee.html', context)


#filter by appoinment date


def filter_employee_by_date(request):
    if request.method == 'GET':
        appointment_date = request.GET.get('appointment_date')

        # Make an API request to filter employees based on the appointment date
        api_url = f'http://127.0.0.1:8000/api/employees/filter/?appointment_date={appointment_date}'
        access_token = request.session['access_token']
        headers = {
            'Authorization': f'Bearer {access_token}',
        }

        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            filtered_employees = response.json()
        else:
            filtered_employees = []

        context = {
            'recent_employees': filtered_employees,
        }
        return render(request, 'employee.html', context)



# sort by gender api req


def sort_employee_by_gender(request):
    if request.method == 'GET':
        gender = request.GET.get('gender')

        # Make an API request to sort employees based on gender
        api_url = f'http://127.0.0.1:8000/api/employees/sort/?gender={gender}'

        access_token = request.session['access_token']
        headers = {
            'Authorization': f'Bearer {access_token}',
        }

        response = requests.get(api_url,headers=headers)
        if response.status_code == 200:
            sorted_employees = response.json()
        else:
            sorted_employees = []

        context = {
            'recent_employees': sorted_employees,
        }
        return render(request, 'employee.html', context)

#success and error page view
def success(request):
    return render(request, 'success.html')

def error(request):
    return render(request, 'error.html')

#Employee Registration 

def register_employee(request):
    url = 'http://127.0.0.1:8000/api/employees/register/'

    if request.method == 'POST':
        # Extract data from the request body
        name = request.POST['name']
        employee_id = request.POST['employee_id']
        gender = request.POST['gender']
        dob = request.POST['dob']
        designation = request.POST['designation']
        department = request.POST['department']
        appointment_date = request.POST['appointment_date']

         # Print the values for debugging
        print(f"name: {name}")
        print(f"employee_id: {employee_id}")
        print(f"gender: {gender}")
        print(f"dob: {dob}")
        print(f"designation: {designation}")
        print(f"department: {department}")
        print(f"appointment_date: {appointment_date}")

        # Request payload
        payload = {
            'name': name,
            'employee_id': employee_id,
            'gender': gender,
            'dob': dob,
            'designation': designation,
            'department': department,
            'appointment_date': appointment_date,
        }

        # Send the POST request to the API endpoint
        response = requests.post(url, data=payload)

        if response.status_code == 201:
            # Employee registration successful
            return redirect('frontend:success') 
        else:
            # Handle the case when the API request returns a non-201 status code
            return redirect('frontend:error') 

    return render(request, 'index.html') 










from django.db import models

# class Department(models.Model):
#     department_id = models.AutoField(primary_key=True)
#     department_name = models.CharField(max_length=255)

#     def __str__(self):
#         return self.department_name

class Employee(models.Model):
    name = models.CharField(max_length=255)
    employee_id = models.IntegerField(primary_key=True)
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dob = models.DateField()
    designation = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    appointment_date = models.DateField()

    def __str__(self):
        return self.name
    

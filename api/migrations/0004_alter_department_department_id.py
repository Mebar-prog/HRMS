# Generated by Django 4.2.1 on 2023-06-05 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_delete_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='department_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]

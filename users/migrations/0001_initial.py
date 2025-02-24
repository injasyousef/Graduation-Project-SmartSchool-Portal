# Generated by Django 5.0.4 on 2024-04-27 10:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('academic', '0001_initial'),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('employeeID', models.AutoField(primary_key=True, serialize=False)),
                ('rule', models.CharField(max_length=255)),
                ('firstName', models.CharField(max_length=255)),
                ('secondName', models.CharField(max_length=255)),
                ('thirdName', models.CharField(max_length=255)),
                ('familyName', models.CharField(max_length=255)),
                ('fullName', models.CharField(max_length=255)),
                ('firstNameOther', models.CharField(max_length=255)),
                ('secondNameOther', models.CharField(max_length=255)),
                ('thirdNameOther', models.CharField(max_length=255)),
                ('familyNameOther', models.CharField(max_length=255)),
                ('fullNameOther', models.CharField(max_length=255)),
                ('identificationNumber', models.IntegerField()),
                ('address', models.TextField()),
                ('major', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=255)),
                ('employmentDate', models.DateField()),
                ('exitDate', models.DateField(blank=True, null=True)),
                ('certificate', models.CharField(max_length=255)),
                ('empolyeeCity', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='empolyee_city', to='common.city')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('studentID', models.AutoField(primary_key=True, serialize=False)),
                ('firstName', models.CharField(max_length=255)),
                ('secondName', models.CharField(max_length=255)),
                ('thirdName', models.CharField(max_length=255)),
                ('familyName', models.CharField(max_length=255)),
                ('fullName', models.CharField(max_length=255)),
                ('firstNameOther', models.CharField(max_length=255)),
                ('secondNameOther', models.CharField(max_length=255)),
                ('thirdNameOther', models.CharField(max_length=255)),
                ('familyNameOther', models.CharField(max_length=255)),
                ('fullNameOther', models.CharField(max_length=255)),
                ('identificationNumber', models.IntegerField()),
                ('address', models.TextField()),
                ('birthDate', models.DateField()),
                ('parentFullName', models.CharField(max_length=255)),
                ('parentIdentificationNumber', models.IntegerField()),
                ('parentNeighborhood', models.CharField(max_length=255)),
                ('parentAddress', models.TextField()),
                ('parentPhone', models.CharField(max_length=255)),
                ('parentEmail', models.EmailField(max_length=254)),
                ('motherName', models.CharField(max_length=255)),
                ('motherPhone', models.CharField(max_length=255)),
                ('motherIdentificationNumber', models.IntegerField()),
                ('fatherIdentificationNumber', models.IntegerField()),
                ('studentPhone', models.CharField(max_length=255)),
                ('studentEmail', models.EmailField(max_length=254)),
                ('numberOfFamilyMembers', models.IntegerField()),
                ('socialStatus', models.CharField(max_length=255)),
                ('healthStatus', models.CharField(max_length=255)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.city')),
                ('currentClass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='current_class', to='academic.class')),
                ('currentSection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='current_section', to='academic.section')),
                ('currentYear', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='current_year', to='academic.studyyear')),
                ('parentCity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_city', to='common.city')),
                ('parentJob', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.parentjob')),
                ('religion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.religion')),
            ],
        ),
        migrations.CreateModel(
            name='UserEmployee',
            fields=[
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.employee')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('isActive', models.BooleanField()),
                ('Financialactive', models.BooleanField()),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.studyyear')),
            ],
        ),
        migrations.CreateModel(
            name='UserStudent',
            fields=[
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.student')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('parentUsername', models.CharField(max_length=255)),
                ('parentPassword', models.CharField(max_length=255)),
                ('isActive', models.BooleanField()),
                ('Financialactive', models.BooleanField()),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.studyyear')),
            ],
        ),
    ]

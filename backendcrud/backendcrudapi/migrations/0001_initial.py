# Generated by Django 4.2.5 on 2023-10-01 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('contact_email', models.EmailField(max_length=254)),
                ('acquired_on', models.DateField()),
                ('customer_status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], max_length=10)),
            ],
        ),
    ]

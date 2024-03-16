# Generated by Django 5.0.1 on 2024-02-28 13:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0002_therapist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('appointmentType', models.CharField(max_length=100)),
                ('note', models.TextField(blank=True, null=True)),
                ('therapist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Auth.therapist')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Auth.customuser')),
            ],
        ),
    ]
# Generated by Django 5.0.1 on 2024-02-19 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Therapist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='/static/images/img_1.jpg', upload_to='media/')),
                ('name', models.CharField(max_length=20)),
                ('price', models.CharField(max_length=30)),
                ('speciality', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1000)),
            ],
        ),
    ]

# Generated by Django 4.1.4 on 2022-12-16 00:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mat_no', models.CharField(max_length=15)),
                ('street_address', models.TextField(max_length=300)),
                ('city', models.TextField(max_length=150)),
                ('state', models.TextField(max_length=150)),
                ('slug', models.SlugField(unique=True)),
                ('lat', models.CharField(blank=True, max_length=20, null=True)),
                ('long', models.CharField(blank=True, max_length=20, null=True)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.department')),
                ('stud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

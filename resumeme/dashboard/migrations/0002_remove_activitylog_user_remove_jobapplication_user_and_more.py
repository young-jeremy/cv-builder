# Generated by Django 5.1.7 on 2025-03-26 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="activitylog",
            name="user",
        ),
        migrations.RemoveField(
            model_name="jobapplication",
            name="user",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="user",
        ),
        migrations.RemoveField(
            model_name="savedsection",
            name="user",
        ),
        migrations.RemoveField(
            model_name="subscription",
            name="user",
        ),
        migrations.RemoveField(
            model_name="template",
            name="favorited_by",
        ),
        migrations.RemoveField(
            model_name="userdashboardsettings",
            name="user",
        ),
    ]

# Generated by Django 5.1.7 on 2025-04-04 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("templates_app", "0003_resumetemplate_is_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="resumetemplate",
            name="color_scheme",
            field=models.CharField(default="blue", max_length=50),
        ),
    ]

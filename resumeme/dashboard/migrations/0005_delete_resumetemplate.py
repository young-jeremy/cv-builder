# Generated by Django 5.1.7 on 2025-04-08 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0004_delete_usertemplateselection"),
    ]

    operations = [
        migrations.DeleteModel(
            name="ResumeTemplate",
        ),
    ]

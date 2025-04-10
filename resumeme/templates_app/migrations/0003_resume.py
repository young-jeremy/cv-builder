# Generated by Django 5.1.7 on 2025-04-08 12:42

import django.db.models.deletion
import phonenumber_field.modelfields
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("templates_app", "0002_resumetemplate_category_resumetemplate_color_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Resume",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("title", models.CharField(max_length=100)),
                (
                    "status",
                    models.CharField(
                        choices=[("draft", "Draft"), ("published", "Published")],
                        default="draft",
                        max_length=20,
                    ),
                ),
                ("content", models.JSONField(default=dict)),
                ("custom_css", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=128, null=True, region=None
                    ),
                ),
                ("location", models.CharField(blank=True, max_length=100, null=True)),
                ("headline", models.TextField(blank=True, null=True)),
                ("summary", models.TextField(blank=True, null=True)),
                (
                    "template",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="resumes",
                        to="templates_app.resumetemplate",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="resumes",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Resume",
                "verbose_name_plural": "Resumes",
                "ordering": ["-created_at"],
            },
        ),
    ]

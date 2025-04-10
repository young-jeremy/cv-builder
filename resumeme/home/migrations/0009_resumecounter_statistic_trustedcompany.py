# Generated by Django 5.1.7 on 2025-04-07 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0008_resume_email_resume_headline_resume_location_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ResumeCounter",
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
                ("count", models.IntegerField(default=0)),
                ("last_updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Statistic",
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
                ("title", models.CharField(max_length=100)),
                ("value", models.CharField(max_length=20)),
                ("description", models.TextField()),
                ("order", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="TrustedCompany",
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
                ("name", models.CharField(max_length=100)),
                ("logo", models.ImageField(upload_to="company_logos/")),
                ("order", models.IntegerField(default=0)),
            ],
            options={
                "verbose_name_plural": "Trusted Companies",
            },
        ),
    ]

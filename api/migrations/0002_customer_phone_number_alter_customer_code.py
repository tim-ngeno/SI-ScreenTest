# Generated by Django 5.1.1 on 2024-09-19 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="phone_number",
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name="customer",
            name="code",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]

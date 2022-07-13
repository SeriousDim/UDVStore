# Generated by Django 3.2.12 on 2022-07-11 17:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0012_create_activities"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="balance",
            field=models.DecimalField(
                decimal_places=1, default=0, max_digits=11, validators=[django.core.validators.MinValueValidator(0)]
            ),
        ),
    ]
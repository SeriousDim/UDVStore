# Generated by Django 3.2.12 on 2022-05-12 12:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0007_transaction_related_transaction"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="transaction",
            name="related_transaction",
        ),
        migrations.AddField(
            model_name="transaction",
            name="response",
            field=models.OneToOneField(
                null=True, on_delete=django.db.models.deletion.PROTECT, related_name="request", to="api.transaction"
            ),
        ),
    ]

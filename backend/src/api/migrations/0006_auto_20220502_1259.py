# Generated by Django 3.2.12 on 2022-05-02 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0005_auto_20220424_1904"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="profile",
            options={"ordering": ("pk",), "verbose_name": "Profile", "verbose_name_plural": "Profiles"},
        ),
        migrations.AlterField(
            model_name="transaction",
            name="type",
            field=models.IntegerField(
                choices=[
                    (1, "Buying"),
                    (2, "Deposit"),
                    (3, "Coin Gifting"),
                    (4, "Request"),
                    (5, "Canceled"),
                    (6, "Approved"),
                ],
                default=1,
            ),
        ),
    ]
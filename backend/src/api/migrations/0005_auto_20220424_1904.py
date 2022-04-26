# Generated by Django 3.2.12 on 2022-04-24 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20220421_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storagecell',
            name='size',
            field=models.IntegerField(choices=[(0, 'None'), (1, 'Xs'), (2, 'S'), (3, 'M'), (4, 'L'), (5, 'Xl'), (6, 'Xxl'), (7, 'Xxxl')], default=0),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.IntegerField(choices=[(1, 'Buying'), (2, 'Deposit'), (3, 'Coin Gifting'), (4, 'Accept')], default=1),
        ),
    ]
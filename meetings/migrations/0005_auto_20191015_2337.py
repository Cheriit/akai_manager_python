# Generated by Django 2.2.5 on 2019-10-15 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0004_delete_attendance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]

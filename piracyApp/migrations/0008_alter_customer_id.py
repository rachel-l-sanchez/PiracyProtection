# Generated by Django 4.1.5 on 2023-02-01 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('piracyApp', '0007_rename_user_customer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='id',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
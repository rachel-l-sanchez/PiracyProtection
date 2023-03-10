# Generated by Django 2.2.11 on 2023-01-27 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('piracyApp', '0004_auto_20230122_2216'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='stripe_file_id',
            field=models.CharField(default='defaultID', max_length=100),
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_price_id', models.CharField(max_length=100)),
                ('price', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='piracyApp.File')),
            ],
        ),
    ]

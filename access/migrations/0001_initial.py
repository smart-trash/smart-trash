# Generated by Django 4.0.4 on 2022-06-07 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ForgotPassword',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=100)),
            ],
        ),
    ]
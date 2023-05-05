# Generated by Django 4.0.4 on 2022-06-07 13:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('smartbin', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Assigned', 'Assigned '), ('Collected', 'Collected'), ('Verified', 'Verified')], max_length=10)),
                ('type', models.CharField(choices=[('Manual', 'Manual'), ('Automatic', 'Automatic')], default='Automatic', max_length=10)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('collection_date', models.DateField(null=True)),
                ('collection_agent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('smartbin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartbin.smartbin')),
            ],
        ),
    ]

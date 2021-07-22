# Generated by Django 3.2.5 on 2021-07-22 21:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('juggle', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professional',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='businessadmin',
            unique_together={('user', 'business')},
        ),
        migrations.AlterUniqueTogether(
            name='jobapplication',
            unique_together={('job', 'professional')},
        ),
    ]
# Generated by Django 4.1.7 on 2024-03-10 20:14

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Events",
            new_name="Event",
        ),
    ]
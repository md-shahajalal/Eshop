# Generated by Django 2.2.3 on 2021-12-13 11:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('EbazarApp', '0003_auto_20211212_2349'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_owner',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]

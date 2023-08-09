# Generated by Django 4.2.3 on 2023-08-08 13:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0009_alter_order_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalPaid', models.IntegerField()),
                ('dateCreated', models.DateTimeField()),
                ('status', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderHistoryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('history', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.orderhistory')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.productitem')),
            ],
        ),
    ]

# Generated by Django 4.2.3 on 2023-07-31 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_product_dateadded'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='photo',
            field=models.ImageField(null=True, upload_to='uploads/'),
        ),
    ]

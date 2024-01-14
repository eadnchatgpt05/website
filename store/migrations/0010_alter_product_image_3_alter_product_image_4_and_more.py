# Generated by Django 4.1.4 on 2023-08-25 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_promotion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image_3',
            field=models.ImageField(blank=True, null=True, upload_to='products/images/list/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_4',
            field=models.ImageField(blank=True, null=True, upload_to='products/images/list/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_5',
            field=models.ImageField(blank=True, null=True, upload_to='products/images/list/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='promotion',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]

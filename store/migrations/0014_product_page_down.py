# Generated by Django 4.1.4 on 2023-08-25 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_product_page_left'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product_Page_Down',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='store.product')),
            ],
        ),
    ]

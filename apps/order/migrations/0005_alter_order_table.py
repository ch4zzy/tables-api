# Generated by Django 4.2 on 2023-05-08 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_alter_order_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='order.table'),
        ),
    ]
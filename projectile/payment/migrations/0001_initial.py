# Generated by Django 5.0.1 on 2024-01-22 10:20

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('DRAFT', 'DRAFT'), ('REMOVED', 'Removed')], db_index=True, default='ACTIVE', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('payment_type', models.CharField(choices=[('UNDEFINED', 'Undefined'), ('CASH_ON_DELIVERY', 'Cash_On_Delivery'), ('ONLINE_PAYMENT', 'Online_Payment')], default='UNDEFINED', max_length=20)),
                ('total_payable', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_paid', models.BooleanField(default=False)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='order.shoporder')),
            ],
            options={
                'verbose_name': 'Order Payment',
                'verbose_name_plural': 'Order Payments',
            },
        ),
    ]
# Generated by Django 5.0.1 on 2024-01-18 15:38

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('DRAFT', 'DRAFT'), ('REMOVED', 'Removed')], db_index=True, default='ACTIVE', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(db_index=True, max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('website', models.URLField(blank=True, help_text="URL of the shop's website", null=True)),
                ('established_date', models.DateField(blank=True, help_text='Date when the shop was established', null=True)),
                ('domain', models.CharField(blank=True, db_index=True, max_length=255, null=True, unique=True)),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_merchant', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Merchant Shop',
                'verbose_name_plural': 'Merchant Shops',
            },
        ),
        migrations.CreateModel(
            name='ShopUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('DRAFT', 'DRAFT'), ('REMOVED', 'Removed')], db_index=True, default='ACTIVE', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_role', models.CharField(choices=[('UNDEFINED', 'Undefined'), ('MERCHANT', 'Merchant'), ('MANAGER', 'Manager'), ('CASHIER', 'Cashier'), ('DELIVERER', 'Deliverer')], default='UNDEFINED', max_length=20)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='merchant_shop_user', to='shop.shop')),
                ('shop_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Merchant Shop User',
                'verbose_name_plural': 'Merchant Shop Users ',
            },
        ),
        migrations.AddConstraint(
            model_name='shopuser',
            constraint=models.UniqueConstraint(fields=('shop_user', 'user_role'), name='unique_shop_user_role'),
        ),
    ]

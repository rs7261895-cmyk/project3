# Generated initial migration for ConstructionMart store models.
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=140)),
                ("category", models.CharField(choices=[("cement", "Cement"), ("steel", "Steel"), ("bricks", "Bricks"), ("sand", "Sand & Aggregates"), ("other", "Other")], default="other", max_length=20)),
                ("description", models.TextField(blank=True)),
                ("unit", models.CharField(default="unit", max_length=30)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("stock", models.PositiveIntegerField(default=0)),
                ("supplier_name", models.CharField(default="ConstructionMart Supplier", max_length=140)),
                ("image_url", models.URLField(blank=True)),
            ],
            options={"ordering": ["category", "name"]},
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("customer_name", models.CharField(max_length=140)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=30)),
                ("delivery_address", models.TextField()),
                ("status", models.CharField(choices=[("placed", "Order placed"), ("confirmed", "Confirmed"), ("dispatched", "Dispatched"), ("delivered", "Delivered")], default="placed", max_length=20)),
                ("total", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantity", models.PositiveIntegerField()),
                ("unit_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="store.order")),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="store.product")),
            ],
        ),
    ]

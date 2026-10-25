from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ("cement", "Cement"),
        ("steel", "Steel"),
        ("bricks", "Bricks"),
        ("sand", "Sand & Aggregates"),
        ("other", "Other"),
    ]
    name = models.CharField(max_length=140)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="other")
    description = models.TextField(blank=True)
    unit = models.CharField(max_length=30, default="unit")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    supplier_name = models.CharField(max_length=140, default="ConstructionMart Supplier")
    image_url = models.URLField(blank=True)

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ("placed", "Order placed"),
        ("confirmed", "Confirmed"),
        ("dispatched", "Dispatched"),
        ("delivered", "Delivered"),
    ]
    customer_name = models.CharField(max_length=140)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    delivery_address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="placed")
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk} - {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def line_total(self):
        return self.quantity * self.unit_price

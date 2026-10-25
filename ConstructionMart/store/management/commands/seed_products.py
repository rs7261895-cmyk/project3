from django.core.management.base import BaseCommand
from store.models import Product


class Command(BaseCommand):
    help = "Create the sample construction materials if they do not already exist."

    def handle(self, *args, **options):
        products = [
            ("OPC Cement 50kg", "cement", "Standard 50 kg cement bag. Sample listing.", "bag", "400.00", 250, "ABC Cement Supply"),
            ("PPC Cement 50kg", "cement", "PPC cement, 50 kg bag. Sample listing.", "bag", "380.00", 180, "SouthBuild Traders"),
            ("TMT Steel Rod 8mm", "steel", "8 mm TMT reinforcement bar. Price shown per kg.", "kg", "68.00", 1200, "Metro Steel Depot"),
            ("TMT Steel Rod 12mm", "steel", "12 mm TMT reinforcement bar. Price shown per kg.", "kg", "70.00", 900, "Metro Steel Depot"),
            ("Red Clay Brick", "bricks", "Common red clay brick. Sample listing.", "piece", "9.00", 10000, "Madurai Brick Works"),
            ("M-Sand", "sand", "Manufactured sand. Price shown per cubic foot.", "cu ft", "55.00", 800, "GreenRock Aggregates"),
            ("Blue Metal Aggregate", "sand", "Construction aggregate. Price shown per cubic foot.", "cu ft", "48.00", 600, "GreenRock Aggregates"),
        ]
        created = 0
        for name, category, description, unit, price, stock, supplier in products:
            _, was_created = Product.objects.get_or_create(
                name=name,
                defaults={
                    "category": category,
                    "description": description,
                    "unit": unit,
                    "price": price,
                    "stock": stock,
                    "supplier_name": supplier,
                },
            )
            created += int(was_created)
        self.stdout.write(
            self.style.SUCCESS(f"Sample products ready. Created {created} new product(s).")
        )

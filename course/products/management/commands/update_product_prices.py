from _decimal import Decimal
from django.core.management.base import BaseCommand

from ...models import Product


class Command(BaseCommand):
    help = 'Update product prices by applying a percentage increase'

    def add_arguments(self, parser):
        parser.add_argument('percentage_increase', type=float, help='Percentage increase for product prices')

    def handle(self, *args, **options):
        percentage_increase = options['percentage_increase']

        if percentage_increase <= 0:
            self.stdout.write(self.style.ERROR('Percentage increase should be a positive number.'))
            return

        try:
            products = Product.objects.all()
            updated_products = 0

            for product in products:
                updated_price = product.price * Decimal(1 + percentage_increase / 100)
                product.price = updated_price
                product.save()
                updated_products += 1

            self.stdout.write(self.style.SUCCESS(f'Successfully updated prices for {updated_products} products.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))

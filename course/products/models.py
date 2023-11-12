from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from simple_history.models import HistoricalRecords


class Category(models.Model):
    name = models.CharField(max_length=100)
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(default=timezone.now)
    categories = models.ManyToManyField(Category, related_name='products')
    availability = models.BooleanField(default=True)
    history = HistoricalRecords()
    stock_quantity = models.PositiveIntegerField(default=0)
    manufacturing_time = models.DurationField(null=True, blank=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    history = HistoricalRecords()

    def update_total_price(self):
        self.total_price = sum(item.subtotal for item in self.cartitem_set.all())
        self.save()

    def __str__(self):
        return f"{self.user}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.cart} | {self.product}"

    @property
    def calculate_subtotal(self):
        return self.quantity * self.product.price

    def save(self, *args, **kwargs):
        self.subtotal = self.calculate_subtotal  # Calculate subtotal
        super().save(*args, **kwargs)


@receiver(post_save, sender=CartItem)
@receiver(post_delete, sender=CartItem)
def update_cart(sender, instance, **kwargs):
    instance.cart.update_total_price()
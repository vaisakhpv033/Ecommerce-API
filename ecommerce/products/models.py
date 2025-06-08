from django.db import models

# Create your models here.
class Products(models.Model):
    """
    Represents a product in the e-commerce application.

    Attributes:
        product_title (CharField): The title of the product (max length: 255).
        product_subtitle (CharField): An optional subtitle for the product (max length: 255).
        description (TextField): A detailed description of the product.
        price (DecimalField): The price of the product with up to 10 digits and 2 decimal places.
        image (URLField): An optional URL to the product's image.
        stock (PositiveIntegerField): The number of items available in stock (default: 0).
        is_available (BooleanField): Indicates whether the product is available for purchase (default: True).
        created_at (DateTimeField): The timestamp when the product was created (auto-generated).
        updated_at (DateTimeField): The timestamp when the product was last updated (auto-updated).
    """

    product_title = models.CharField(max_length=255)
    product_subtitle = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns a string representation of the product.

        Returns:
            str: The title of the product.
        """
        return self.product_title
from django.db import models
from accounts.validators import phone_number_validator

# Create your models here.
class Cart(models.Model):
    """
    Represents a shopping cart in the e-commerce application.

    Attributes:
        user (ForeignKey): The user associated with the cart.
        created_at (DateTimeField): The timestamp when the cart was created (auto-generated).
        updated_at (DateTimeField): The timestamp when the cart was last updated (auto-updated).
    """

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='carts')
    product = models.ForeignKey('products.Products', on_delete=models.CASCADE, related_name='carts')
    quantity = models.PositiveIntegerField(default=1, help_text="Quantity of the product in the cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns a string representation of the cart.

        Returns:
            str: A string indicating the user's username associated with the cart.
        """
        return f"Cart for {self.user.email}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"], name="unique_user_product_cart"
            )
        ]
        verbose_name_plural = "Cart"
        ordering = ["-created_at"]


class Addresses(models.Model):
    """
    Represents a user's address in the e-commerce application.

    Attributes:
        user (ForeignKey): The user associated with the address.
        address_line_1 (CharField): The first line of the address.
        address_line_2 (CharField, optional): The second line of the address (optional).
        city (CharField): The city of the address.
        state (CharField): The state of the address.
        postal_code (CharField): The postal code of the address.
        country (CharField): The country of the address.
        created_at (DateTimeField): The timestamp when the address was created (auto-generated).
        updated_at (DateTimeField): The timestamp when the address was last updated (auto-updated).
    """

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='addresses')
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, validators=[phone_number_validator])
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def full_address(self):
        return f"{self.address_line_1}, {self.address_line_2 or ''}, {self.city}, {self.state}, {self.postal_code}, {self.country}"

    def __str__(self):
        """
        Returns a string representation of the address.

        Returns:
            str: A string indicating the user's email and city associated with the address.
        """
        return f"{self.user.email} - {self.city}"
    
    class Meta:
        verbose_name_plural = "Addresses"
        ordering = ["-created_at"]
from django.db import models

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
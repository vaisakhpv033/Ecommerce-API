from django.db import models
from django.db import IntegrityError
from django.utils import timezone
import uuid

# Create your models here.
class Order(models.Model):
    """
    Represents a user's order containing one or multiple products.

    """

    class OrderStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"
        REFUNDED = "refunded", "Refunded"

    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    order_number = models.CharField(max_length=255, unique=True, db_index=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(
        max_length=10, choices=OrderStatus.choices, default=OrderStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


        
    def generate_transaction_no(self):
        """
        Generates a unique order number using timestamp and UUID
        """

        unique_id = uuid.uuid4().hex[:12].upper()
        timestamp = timezone.now().strftime("%y%m%d%H%M%S")
        return f"{timestamp}{unique_id}"
    
    def save(self, *args, **kwargs):
        """
        Ensure transaction number generation on creation and handle duplicates
        """

        if self._state.adding and not self.order_number:
            for _ in range(5): # retry upto 5 times in case of collision
                self.order_number = self.generate_transaction_no()
                try:
                    super().save(*args, **kwargs)
                    return 
                except IntegrityError:
                    continue
            raise IntegrityError('Failed to generate a unique transaction number')
        else:
            super().save(*args, **kwargs)

    
    def __str__(self):
        return f"{self.user.email} - {self.order_number}"

    class Meta:
        verbose_name_plural = "Orders"
        ordering = ["-created_at"]




class OrderItem(models.Model):
    """
    Represents an individual product within an order.

  
    """

    class OrderItemStatus(models.TextChoices):
        PROCESSING = "processing", "Processing"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"


    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name="items")
    product = models.ForeignKey("products.Products", on_delete=models.SET_NULL, null=True)
    product_title = models.CharField(max_length=255)
    product_subtitle = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1, help_text="Quantity of the product in the order")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=OrderItemStatus.choices, default=OrderItemStatus.PROCESSING
    )
    is_refunded = models.BooleanField(default=False)
    refund_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    refund_initiated_at = models.DateTimeField(null=True, blank=True)
    refund_completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        """
        Calculate the total price for this order item based on quantity and product price.
        """
        return (self.price or 0) * self.quantity

    def set_product_details(self):
        if not self.product_title:
            self.product_title = self.product.product_title
        if not self.product_subtitle:
            self.product_subtitle = self.product.product_subtitle
        if not self.price:
            self.price = self.product.price


    def save(self, *args, **kwargs):
        self.set_product_details()
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.order.order_number} - {self.product.product_title}"

    class Meta:
        verbose_name_plural = "Order Items"
        ordering = ["-created_at"]

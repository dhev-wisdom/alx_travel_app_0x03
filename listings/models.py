from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

# Create your models here.

User = get_user_model()

class Listing(models.Model):
    """
    Table that stores Listings
    """
    listing_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    listing_name = models.CharField(max_length=50)
    listing_description = models.TextField()
    image_url = models.URLField(max_length=555, blank=True, null=True)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.listing_name


class Booking(models.Model):
    """
    Models that stores Listing Bookings
    """
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20,
                              choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'),
                                       ('cancelled', 'Cancelled')])
    booked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="booking")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.listing.listing_name} by {self.booked_by}"



class Review(models.Model):
    """
    Model for reviews for the bookings and properties
    """
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    review_title = models.CharField(max_length=255)
    review_body = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5,
                                              validators=[MinValueValidator(1),
                                                          MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"({self.booking.listing.listing_name}): {self.author} - {self.review_title}"
    

class Payment(models.Model):
    """
    Model for everything relating to payment data
    """
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    payer_email = models.EmailField(max_length=50, null=True, blank=True)
    payer_phone = models.CharField(max_length=20, null=True, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="payments")
    payment_status = models.CharField(max_length=10, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='pending')
    transaction_id = models.CharField(max_length=100, null=True, blank=True, unique=True)
    booking_reference = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booking_reference} by {self.payer.username} - {self.payment_status}"
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from listings.models import Listing, Booking, Review
import random

User = get_user_model()

class Command(BaseCommand):
    """
    Django management command to seed database with dummy data.
    """
    help = "Seed the database with test data"

    def handle(self, *args, **kwargs):
        """main function to handle seed function"""
        self.stdout.write("Seeding data...")

        # Create users
        users = []
        for i in range(3):
            user, created = User.objects.get_or_create(
                username = f"user{i}",
                email = f"user{i}@example.com"
            )
            if created:
                user.set_password("password123")
                user.save()
                users.append(user)

        # Create listings
        listings = []
        for i in range(5):
            listing = Listing.objects.create(
                listing_name = f"Listing {i}",
                listing_description = f"Description for Listing {i}",
                image_url = f"https://placehold.co/600x400?text=Listing+{i}",
                price_per_night = random.randint(50, 1000),
                location = "Lagos, Nigeria",
                host = random.choice(users)
            )
            listings.append(listing)

        # Create bookings
        bookings = []
        for i in range(5):
            start_date = timezone.now().date() + timedelta(days=i)
            end_date = start_date + timedelta(days=3)
            booking = Booking.objects.create(
                listing = random.choice(listings),
                start_date = start_date,
                end_date = end_date,
                status = random.choice(['pending', 'confirmed', 'cancelled']),
                booked_by = random.choice(users)
            )
            bookings.append(booking)

        # Create reviews
        reviews = []
        for i in range(5):
            booking = random.choice(bookings)
            review = Review.objects.create(
                booking = booking,
                review_title = f"Review {i}",
                review_body = f"Review {i} for {booking.listing.listing_name}",
                rating = random.randint(1, 5),
                author = random.choice(users)
            )
            reviews.append(review)

        self.stdout.write(self.style.SUCCESS("Successfully seeded the database with test data"))
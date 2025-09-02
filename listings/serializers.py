from rest_framework import serializers
from .models import Listing, Booking, Review, Payment

class ListingSerializer(serializers.ModelSerializer):
    """
    class converts complex Listing python object to simple json
    that the frontend can consume
    """
    thumbnail_url = serializers.SerializerMethodField()

    def get_thumbnail_url(self, obj):
        return obj.image_url
    
    class Meta:
        model = Listing
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    """
    class converts complex Booking python object to simple json
    that the frontend can consume
    """
    class Meta:
        model = Booking
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """
    class converts complex Review python object to simple json
    that the frontend can consume
    """
    class Meta:
        model = Review
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    """
    class converts complex Review python object to simple json
    that the frontend can consume
    """
    class Meta:
        model = Payment
        fields = '__all__'
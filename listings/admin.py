from django.contrib import admin
from .models import Listing, Booking, Review, Payment

# Register your models here.
admin.site.register(Listing)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register({Payment})
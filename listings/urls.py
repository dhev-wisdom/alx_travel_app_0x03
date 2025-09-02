from django.urls import path, include
from .views import ListingViewSet, BookingViewSet, ReviewViewSet, PaymentViewSet, initiate_payment, verify_payment
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listing')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'payments', PaymentViewSet, basename='payment')
# router.register(r'initiate_payment', InitiatePaymentView, basename='initiate-payment')
# router.register(r'verify_payment', VerifyPaymentView, basename='verify-payment')

urlpatterns = [
    path('', include(router.urls)),
    path("initiate-payment/", initiate_payment, name="initiate-payment"),
    path("verify-payment/", verify_payment, name="verify-payment")
]
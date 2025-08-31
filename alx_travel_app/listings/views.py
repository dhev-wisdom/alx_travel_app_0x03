from django.shortcuts import render, get_object_or_404
from django.conf import settings
from rest_framework.viewsets import ModelViewSet
from .serializers import ListingSerializer, BookingSerializer, ReviewSerializer, PaymentSerializer
from .models import Listing, Booking, Review, Payment
from .tasks import send_booking_confirmation_email, send_payment_confirmation_email
from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import uuid

# Create your views here.
class ListingViewSet(ModelViewSet):
    """view for the Listing model"""
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Listing.objects.all()


class BookingViewSet(ModelViewSet):
    """view for the Booking model"""
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Booking.objects.all()

    def perform_create(self, serializer):
        booking = serializer.save()

        booking_details = f"Booking ID: {booking.booking_id}\nDate: {booking.created_at}\nBooked by: {booking.booked_by}"
        print("Booking details: ", booking_details)
        print("Booker: ", booking.booked_by.email)
        print("Email Host Password: ", settings.EMAIL_HOST_PASSWORD)
        send_booking_confirmation_email.delay(user_email=booking.booked_by.email, booking_details=booking_details)

        return booking


class ReviewViewSet(ModelViewSet):
    """view for the Review model"""
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Review.objects.all()


class PaymentViewSet(ModelViewSet):
    """view for the Review model"""
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Payment.objects.all()


# class InitiatePaymentView(APIView):
#     """Class-based view to initiate payment"""
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         amount = request.data.get("amount")
#         email = request.data.get("email")
#         booking_id = request.data.get("booking_id")

#         if not all([amount, email, booking_id]):
#             return Response(
#                 {"error": "amount, email and booking_id are required"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         booking = get_object_or_404(Booking, booking_id=booking_id)

#         payment = Payment.objects.create(
#             payer=request.user,
#             amount=amount,
#             booking=booking,
#         )

#         headers = {
#             "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
#             "Content-Type": "application/json",
#         }

#         data = {
#             "amount": str(amount),
#             "currency": "USD",
#             "email": email,
#             "tx_ref": str(payment.booking_reference),
#             "callback_url": "http://127.0.0.1:8000/api/verify-payment/",
#         }

#         try:
#             response = requests.post(
#                 f"{settings.CHAPA_BASE_URL}/initialize", json=data, headers=headers
#             )
#             res_data = response.json()
#         except requests.RequestException as e:
#             return Response(
#                 {"error": f"Payment gateway error: {str(e)}"},
#                 status=status.HTTP_502_BAD_GATEWAY,
#             )

#         if res_data.get("status") == "success":
#             payment.transaction_id = res_data["data"]["tx_ref"]
#             payment.save()
#             return Response(
#                 {"checkout_url": res_data["data"]["checkout_url"]},
#                 status=status.HTTP_200_OK,
#             )

#         return Response(res_data, status=status.HTTP_400_BAD_REQUEST)


# class VerifyPaymentView(APIView):
#     """Class-based view to verify payment"""
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         tx_ref = request.query_params.get("tx_ref")

#         if not tx_ref:
#             return Response(
#                 {"error": "tx_ref is required"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         headers = {"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"}

#         try:
#             response = requests.get(
#                 f"{settings.CHAPA_BASE_URL}/verify/{tx_ref}", headers=headers
#             )
#             res_data = response.json()
#         except requests.RequestException as e:
#             return Response(
#                 {"error": f"Payment gateway error: {str(e)}"},
#                 status=status.HTTP_502_BAD_GATEWAY,
#             )

#         try:
#             payment = Payment.objects.get(booking_reference=tx_ref)
#         except Payment.DoesNotExist:
#             return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)

#         if (
#             res_data.get("status") == "success"
#             and res_data["data"]["status"] == "success"
#         ):
#             payment.payment_status = "Completed"
#             payment.save()
#             return Response({"message": "Payment verified successfully"}, status=status.HTTP_200_OK)

#         payment.payment_status = "Failed"
#         payment.save()
#         return Response({"message": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def initiate_payment(request):
    amount = request.data.get('amount')
    email = request.data.get('email')
    booking_id = request.data.get('booking_id')
    first_name = request.data.get('first_name', 'Guest')
    last_name = request.data.get('last_name', '')
    phone_number = request.data.get('phone_number', '')

    booking = get_object_or_404(Booking, booking_id=booking_id)

    payment = Payment.objects.create(
        payer=request.user,
        amount=amount,
        booking=booking,
        payer_email=email,
        payer_phone=phone_number
        )

    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "amount": str(amount),
        "currency": "USD",
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "phone_number": phone_number,
        "tx_ref": str(payment.booking_reference),
        "callback_url": "http://127.0.0.1:8000/api/verify-payment/",
        "customization": {
            "title": "Booking Payment",
            "description": f"Payment for booking"
        }
    }

    response = requests.post(f"{settings.CHAPA_BASE_URL}/initialize", json=data, headers=headers)
    res_data = response.json()

    if res_data.get("status") == "success":
        payment.transaction_id = str(payment.booking_reference)
        payment.save()
        return Response({"checkout_url": res_data["data"]["checkout_url"]})
    
    return Response(res_data, status=400)

@api_view(["GET"])
def verify_payment(request):
    trx_ref = request.query_params.get("trx_ref")

    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
    }

    response = requests.get(f"{settings.CHAPA_BASE_URL}/verify/{trx_ref}", headers=headers)
    res_data = response.json()

    try:
        payment = Payment.objects.get(transaction_id=trx_ref)
    except Payment.DoesNotExist:
        return Response({"error": "Payment not found"}, status=404)
    
    if res_data.get("status") == "success" and res_data["data"]["status"] == "success":
        payment.payment_status = "completed"
        payment.save()
        print("payment ", payment)
        print("payment.payer.email ", payment.payer.email)
        send_payment_confirmation_email.delay(
            user_email=payment.payer_email,
            booking_id=str(payment.booking.booking_id),
            amount=str(payment.amount)
        )
        return Response({"message": "Payment verified successfully"})
    else:
        payment.payment_status = "failed"
        payment.save()
        return Response({"message": "Payment failed"}, status=400)
import logging
from django.conf import settings
from django.core.mail import EmailMessage, get_connection
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer

# Set up logging
logger = logging.getLogger(__name__)

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def create_order(request):
    try:
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()

            # Define the email data
            subject = "Order Confirmation"
            recipient_list = [order.email]
            from_email = settings.MAILERSEND_SMTP_USERNAME
            message = f"<p>Thank you for your order, {order.name}!</p><p>Your order details:</p><p>{order.order_items.all()}</p>"

            # Use Django's default email backend settings
            with get_connection(
                host=settings.MAILERSEND_SMTP_HOST,
                port=settings.MAILERSEND_SMTP_PORT,
                username=settings.MAILERSEND_SMTP_USERNAME,
                password=settings.MAILERSEND_API_KEY,
                use_tls=True
            ) as connection:
                email = EmailMessage(
                    subject=subject,
                    body=message,
                    to=recipient_list,
                    from_email=from_email,
                    connection=connection,
                )
                email.content_subtype = "html"  # Set the email content type to HTML
                email.send()

            logger.info("Email sent successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"Order data is invalid: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.exception("Error processing order")
        return Response({'message': f'Error processing order: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

import logging
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from mailersend import emails

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

            # Construct the email content
            order_items_info = "\n".join(
                [f"{item.quantity} of product ID {item.product_id}" for item in order.order_items.all()]
            )
            subject = 'Order Confirmation'
            html_content = f'<p>Thank you for your order, {order.name}!</p><p>Your order details:</p><p>{order_items_info}</p>'
            plaintext_content = f'Thank you for your order, {order.name}!\n\nYour order details:\n\n{order_items_info}'

            # MailerSend setup
            mailer = emails.NewEmail(settings.MAILERSEND_API_KEY)

            mail_body = {}
            mail_from = {
                "name": "Your Shop Name",
                "email": settings.DEFAULT_FROM_EMAIL,
            }
            recipients = [
                {
                    "name": order.name,
                    "email": order.email,
                }
            ]
            
            # Configure email parameters
            mailer.set_mail_from(mail_from, mail_body)
            mailer.set_mail_to(recipients, mail_body)
            mailer.set_subject(subject, mail_body)
            mailer.set_html_content(html_content, mail_body)
            mailer.set_plaintext_content(plaintext_content, mail_body)

            # Send the email
            mailer.send(mail_body)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"Order data is invalid: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.exception("Error processing order")
        return Response({'message': f'Error processing order: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

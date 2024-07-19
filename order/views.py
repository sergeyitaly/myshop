import logging
from django.conf import settings
from django.core.mail import EmailMessage
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
            order_items = order.order_items.all()  # Fetch related order items

            # Format the order details
            order_details = f"""
            <p>Замовлення: {order.id}</p>
            <p>Ім'я: {order.name}</p>
            <p>Прізвище: {order.surname}</p>
            <p>Телефон: {order.phone}</p>
            <p>Email: {order.email}</p>
            <p>Отримувач той самий: {"Так" if order.receiver else "Ні"}</p>
            <p>Коментар: {order.receiver_comments}</p>
            <p>Створено: {order.submitted_at}</p>
            <p>Пакування як подарунок: {"Так" if order.present else "Ні"}</p>
            """

            # Generate HTML table for order items
            order_items_rows = "".join([
                f"""
                <tr>
                    <td><img src="{item.product.photo.url}" alt="{item.product.name}" style="max-height: 150px; max-width: 150px;" /></td>
                    <td>{item.quantity}</td>
                    <td>{item.product.name}</td>
                    <td>{item.product.price}</td>
                </tr>
                """
                for item in order_items
            ])

            # Calculate the total sum of all order items
            total_sum = sum(item.total_sum for item in order_items)

            order_items_table = f"""
            <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">
                <thead>
                    <tr>
                        <th>Фото</th>
                        <th>Кількість</th>
                        <th>Продукт</th>
                        <th>Ціна</th>
                    </tr>
                </thead>
                <tbody>
                    {order_items_rows}
                </tbody>
            </table>
            """

            # Complete HTML content
            email_body = order_details + "<h3>В замовленні:</h3>" + order_items_table + f"<p><strong>Загальна сума: {total_sum}</strong></p>"

            # Define the email data
            subject = f"KOLORYT Замовлення № {order.id}"
            recipient_list = [order.email]
            from_email = settings.DEFAULT_FROM_EMAIL

            # Send email using EmailMessage for HTML content
            email = EmailMessage(
                subject=subject,
                body=email_body,
                from_email=from_email,
                to=recipient_list
            )
            email.content_subtype = "html"  # Specify that the email body is HTML
            email.send()

            logger.info("Email sent successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"Order data is invalid: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.exception("Error processing order")
        return Response({'message': f'Error processing order: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

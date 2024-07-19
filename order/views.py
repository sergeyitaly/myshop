from django.utils.dateformat import format
from django.utils.timezone import localtime
from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated

# Set up logging
import logging
logger = logging.getLogger(__name__)

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]  # Ensure this matches your settings

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve an order by ID",
        responses={200: OrderSerializer, 404: 'Not Found'}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete an order by ID",
        responses={204: 'No Content', 404: 'Not Found'}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update an order by ID",
        request_body=OrderSerializer,
        responses={200: OrderSerializer, 400: 'Bad Request', 404: 'Not Found'}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_order(request):
    try:
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            order_items = order.order_items.all()  # Fetch related order items

            # Format the order creation datetime with timezone-aware local time
            formatted_date = localtime(order.submitted_at).strftime('%Y-%m-%d %H:%M')

            order_details = f"""
            <p><strong>Замовлення:</strong> {order.id} на сайті <a href='{settings.VERCEL_DOMAIN}'>KOLORYT!</a> </p>
            <p><strong>Ім'я:</strong> {order.name}</p>
            <p><strong>Прізвище:</strong> {order.surname}</p>
            <p><strong>Телефон:</strong> {order.phone}</p>
            <p><strong>Email:</strong> {order.email}</p>
            <p><strong>Отримувач той самий:</strong> {"Так" if order.receiver else "Ні"}</p>
            <p><strong>Коментар:</strong> {order.receiver_comments}</p>
            <p><strong>Створено:</strong> {formatted_date}</p>
            <p><strong>Пакування як подарунок:</strong> {"Так" if order.present else "Ні"}</p>
            """

            # Assume all items have the same currency; get it from the first item
            currency = order_items.first().product.currency if order_items.exists() else "UAH"  # Default to UAH if no items

            # Generate HTML table for order items with columns rearranged
            order_items_rows = "".join([
                f"""
                <tr>
                    <td>{index + 1}</td>
                    <td><img src="{item.product.photo.url}" alt="{item.product.name}" style="width: 50px; height: 50px; object-fit: cover;" /></td>
                    <td>{item.product.name}</td>
                    <td>{item.product.collection.name}</td>
                    <td>{item.quantity}</td>
                    <td>{item.product.size}</td>
                    <td>{item.product.color_name}<br> <div style="width: 10px; height: 10px; background-color: {item.product.color_value}; display: inline-block;"></div></td>
                    <td>{item.product.price} {currency}</td>
                </tr>
                """
                for index, item in enumerate(order_items)
            ])

            # Calculate the total sum of all order items
            total_sum = sum(item.total_sum for item in order_items)

            order_items_table = f"""
            <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">
                <thead>
                    <tr>
                        <th>Номер</th>
                        <th>Фото продукту</th>
                        <th>Назва продукту</th>
                        <th>Колекція</th>
                        <th>Кількість</th>
                        <th>Розмір</th>
                        <th>Колір</th>
                        <th>Ціна</th>
                    </tr>
                </thead>
                <tbody>
                    {order_items_rows}
                </tbody>
            </table>
            """

            # Complete HTML content with total sum and KOLORYT as a link
            email_body = order_details + "<h3><strong>В замовленні:</strong></h3>" + order_items_table + f"<p><strong>Загальна сума: {total_sum} {currency}</strong></p><br><br><p>Дякуємо за замовлення у <a href='{settings.VERCEL_DOMAIN}'>KOLORYT!</a></p><br><p>Менеджер зв'яжеться з Вами скоро за вказаним номером телефону для уточнення деталей замовлення.</p>"

            # Define the email data
            subject = f"KOLORYT. Замовлення № {order.id}"
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

from django.utils.dateformat import format
from django.utils.timezone import localtime
from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from .models import *
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
import logging
import requests
import json
import random
import os
from django.http import JsonResponse
from rest_framework.decorators import action


def health_check(request):
    return JsonResponse({'status': 'ok'})
logger = logging.getLogger(__name__)


class TelegramUserViewSet(viewsets.ModelViewSet):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def create(self, request, *args, **kwargs):
        logger.info(f"Request headers: {request.headers}")
        return super().create(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        phone = request.query_params.get('phone')
        chat_id = request.query_params.get('chat_id')
        if phone and chat_id:
            try:
                user = TelegramUser.objects.get(phone=phone, chat_id=chat_id)
                serializer = self.get_serializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except TelegramUser.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)

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

    @action(detail=False, methods=['get'])
    @swagger_auto_schema(
        operation_description="Retrieve orders by phone number",
        responses={200: OrderSerializer(many=True), 400: 'Bad Request'}
    )
    def by_phone_number(self, request):
        phone_number = request.query_params.get('phone_number', None)
        if not phone_number:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            orders = Order.objects.filter(phone=phone_number)
            serializer = self.get_serializer(orders, many=True)
            return Response({'count': orders.count(), 'results': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching orders: {e}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
def get_random_saying(file_path):
    """Read sayings from a file and return a single random saying."""
    if not os.path.exists(file_path):
        logger.error(f"Failed to read sayings file: [Errno 2] No such file or directory: '{file_path}'")
        return "No sayings available."
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            sayings = [line.strip() for line in file if line.strip()]
        
        if not sayings:
            logger.error("Sayings file is empty.")
            return "No sayings available."
        
        return random.choice(sayings)
    except Exception as e:
        logger.error(f"Error reading sayings file: {e}")
        return "No sayings available."
    
def set_telegram_webhook():
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/setWebhook"
    webhook_url = f"{settings.VERCEL_DOMAIN}/api/telegram_webhook/"  # Ensure this endpoint matches your Django webhook view
    payload = {'url': webhook_url}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    logger.info('Webhook set: %s', response.json())

@method_decorator(csrf_exempt, name='dispatch')
class TelegramWebhook(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            logger.debug(f"Incoming data: {data}")

            chat_id = data['message']['chat']['id']
            contact = data['message'].get('contact')
            if not contact:
                logger.error("No contact information in message")
                return JsonResponse({'status': 'error', 'message': 'No contact information'}, status=400)
            
            phone = contact['phone_number']
            logger.debug(f"Extracted phone: {phone}, chat_id: {chat_id}")

            telegram_user, created = TelegramUser.objects.update_or_create(phone=phone, defaults={'chat_id': chat_id})
            if created:
                logger.debug(f"Created new TelegramUser: {telegram_user}")
            else:
                logger.debug(f"Updated existing TelegramUser: {telegram_user}")

            order = Order.objects.filter(phone=phone).last()  # Get the latest order for the phone number
            if order:
                send_telegram_message(order.id, phone, order.email)

            return JsonResponse({'status': 'ok'})
        except json.JSONDecodeError as e:
            logger.error(f"JSONDecodeError: {e}")
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)
        except KeyError as e:
            logger.error(f"KeyError: {e}")
            return JsonResponse({'status': 'error', 'message': 'Missing required field'}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return JsonResponse({'status': 'error', 'message': 'Internal server error'}, status=500)

telegram_webhook = TelegramWebhook.as_view()

def send_telegram_message(order_id, chat_id, email):
    bot_token = settings.TELEGRAM_BOT_TOKEN
    

    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    
    sayings_file_path = settings.SAYINGS_FILE_PATH
    random_saying = get_random_saying(sayings_file_path)
    
    message = (f"<b>Вітаємо!</b>\n\n"
               f"Ви створили нове замовлення № <b>{order_id}</b> на сайті "
               f"<a href='{settings.VERCEL_DOMAIN}'>KOLORYT</a>.\n"
               f"Деталі замовлення відправлено на email {email}.\n\n"
               f"<i>💬 {random_saying}</i>\n\n"  
               f"<b>Дякуємо, що обрали нас!</b> 🌟")
        
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        result = response.json()
        if not result.get('ok'):
            logger.error(f"Telegram API returned an error: {result.get('description')}")
        return result
    except requests.exceptions.RequestException as e:
        logger.error(f"Request to Telegram API failed: {e}")
        raise
    
@api_view(['POST'])
@permission_classes([AllowAny])
def create_order(request):
    try:
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            order_items = order.order_items.all()  # Fetch related order items

            formatted_date = localtime(order.submitted_at).strftime('%Y-%m-%d %H:%M')

            order_details = f"""
            <p><strong>Замовлення:</strong> № {order.id} на сайті <a href='{settings.VERCEL_DOMAIN}'>KOLORYT!</a></p>
            <p><strong>Ім'я:</strong> {order.name}</p>
            <p><strong>Прізвище:</strong> {order.surname}</p>
            <p><strong>Телефон:</strong> {order.phone}</p>
            <p><strong>Email:</strong> {order.email}</p>
            <p><strong>Отримувач той самий:</strong> {"Ні" if order.receiver else "Так"}</p>
            <p><strong>Коментар:</strong> {order.receiver_comments}</p>
            <p><strong>Створено:</strong> {formatted_date}</p>
            <p><strong>Пакування як подарунок:</strong> {"Так" if order.present else "Ні"}</p>
            """

            if order_items.exists():
                currency = order_items.first().product.currency
            else:
                currency = "UAH"  # Default currency if no order items exist

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

            unsubscribe_link = settings.VERCEL_DOMAIN  # Change to actual unsubscribe URL if available
            email_body = f"""
            <html>
            <head>
                <style>
                    /* Add any CSS styling here */
                </style>
            </head>
            <body>
                <h2>Підтвердження замовлення #{order.id} на сайті KOLORYT</h2>
                {order_details}
                {order_items_table}
                <p><strong>Разом:</strong> {total_sum} {currency}</p>
                <p>Якщо у вас є питання, не вагайтеся зв'язатися з нами.</p>
                <p>З найкращими побажаннями,<br>
                Команда <a href='{settings.VERCEL_DOMAIN}'>KOLORYT</a></p>
                <p><a href='{unsubscribe_link}'>Відмовитися від підписок</a></p>
            </body>
            </html>
            """

            email = EmailMessage(
                subject=f'Підтвердження замовлення #{order.id}',
                body=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[order.email],
                headers={'Content-Type': 'text/html; charset=utf-8'}
            )
            email.content_subtype = "html"
            email.send(fail_silently=False)
            
            # Handle sending a Telegram message
            phone = order.phone
            try:
                telegram_user = TelegramUser.objects.get(phone=phone)
                chat_id = telegram_user.chat_id
                telegram_message = f"Ваше замовлення №{order.id} було успішно створено. Дякуємо за покупку!"
                send_telegram_message(order.id, chat_id, telegram_message)
            except TelegramUser.DoesNotExist:
                logger.warning(f"TelegramUser with phone {phone} not found. No Telegram message sent.")

            return Response({'status': 'Order created', 'order_id': order.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error fetching order: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    phone_number = request.query_params.get('phone_number', None)
    if not phone_number:
        return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        orders = Order.objects.filter(phone=phone_number)
        serializer = OrderSerializer(orders, many=True)
        return Response({'count': orders.count(), 'results': serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching orders: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
import os
import random
import logging
import json
import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import localtime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .models import Order, OrderItem, TelegramUser
from .serializers import OrderSerializer, OrderItemSerializer

logger = logging.getLogger(__name__)
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
@csrf_exempt
def telegram_webhook(request):
    """Handle incoming Telegram webhook updates."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logger.debug(f"Webhook Data: {data}")

            message = data.get('message', {})
            chat_id = message.get('chat', {}).get('id')
            text = message.get('text', '')
            contact = message.get('contact', {})

            if chat_id and contact.get('phone_number'):
                phone_number = contact.get('phone_number')
                update_chat_id(phone_number, chat_id)
                reply_to_user(chat_id, "Thank you! Your phone number has been recorded.")
            elif chat_id and text.startswith('/start'):
                reply_to_user(chat_id, "Welcome! Please send your phone number.")
            else:
                logger.warning("Message received without phone number or invalid command.")

            return JsonResponse({'status': 'ok'})
        except json.JSONDecodeError:
            logger.error("Failed to decode JSON from webhook request.")
            return JsonResponse({'status': 'invalid JSON'}, status=400)
        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            return JsonResponse({'status': 'error'}, status=500)

    return JsonResponse({'status': 'invalid request'}, status=400)

def update_chat_id(phone, chat_id):
    """Update or create a Telegram user with the given chat ID."""
    user, created = TelegramUser.objects.get_or_create(phone=phone)
    user.chat_id = chat_id
    user.save()
    logger.info(f"Updated chat ID for phone: {phone}")

def reply_to_user(chat_id, text):
    """Send a reply message to a Telegram user."""
    url = f'https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text,
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        result = response.json()
        if not result.get('ok'):
            logger.error(f"Telegram API returned an error: {result.get('description')}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request to Telegram API failed: {e}")



def get_telegram_chat_id(phone):
    """Retrieve the chat ID for a given phone number."""
    try:
        user = TelegramUser.objects.get(phone=phone)
        return user.chat_id
    except TelegramUser.DoesNotExist:
        logger.error(f"Chat ID not found for phone number: {phone}")
        return None

def send_telegram_message(order_id, chat_id, email):
    """Send a message to a Telegram user with order details."""
    bot_token = settings.TELEGRAM_BOT_TOKEN
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    
    random_saying = get_random_saying(settings.SAYINGS_FILE_PATH)

    message = (f"<b>Вітаємо!</b>\n\n"
               f"Ви створили нове замовлення № <b>{order_id}</b> на сайті "
               f"<a href='{settings.VERCEL_DOMAIN}'>KOLORYT</a>.\n"
               f"Деталі замовлення відправлено на email: <b>{email}</b>.\n\n"
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
    except requests.exceptions.RequestException as e:
        logger.error(f"Request to Telegram API failed: {e}")
        if response:
            logger.debug(f"Response content: {response.content}")

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
    """Create an order and send a confirmation message to Telegram."""
    try:
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            order_items = order.order_items.all()

            formatted_date = localtime(order.submitted_at).strftime('%Y-%m-%d %H:%M')

            order_details = f"""
            <p><strong>Замовлення:</strong> № {order.id} на сайті <a href='{settings.VERCEL_DOMAIN}'>KOLORYT!</a></p>
            <p><strong>Ім'я:</strong> {order.name}</p>
            <p><strong>Прізвище:</strong> {order.surname}</p>
            <p><strong>Телефон:</strong> {order.phone}</p>
            <p><strong>Email:</strong> {order.email}</p>
            <p><strong>Отримувач той самий:</strong> {"Ні" if not order.receiver else "Так"}</p>
            <p><strong>Коментар:</strong> {order.receiver_comments}</p>
            <p><strong>Створено:</strong> {formatted_date}</p>
            <p><strong>Пакування як подарунок:</strong> {"Так" if order.present else "Ні"}</p>
            """

            currency = order_items.first().product.currency if order_items.exists() else "UAH"

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

            order_details += f"""
            <p><strong>Всього товарів:</strong> {len(order_items)}</p>
            <p><strong>Загальна сума:</strong> {total_sum} {currency}</p>
            """

            email_body = f"""
            <html>
            <body>
                <h2>Ваше замовлення!</h2>
                {order_details}
                <h3>Деталі замовлення:</h3>
                <table border="1" cellpadding="5" cellspacing="0">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Фото</th>
                            <th>Назва</th>
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
            </body>
            </html>
            """

            # Send Telegram message
            chat_id = get_telegram_chat_id(order.phone)
            if chat_id:
                send_telegram_message(order.id, chat_id, order.email)

            # Send email
            email_message = EmailMessage(
                subject=f"Ваше замовлення № {order.id}",
                body=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[order.email],
            )
            email_message.content_subtype = 'html'
            email_message.send()

            return Response({'status': 'Order created successfully.'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"Error creating order: {e}")
        return Response({'status': 'error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

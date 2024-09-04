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
from .signals import update_order_status_with_notification
from django.http import JsonResponse, Http404


logger = logging.getLogger(__name__)
def health_check(request):
    return JsonResponse({'status': 'ok'})

class OrderSummaryViewSet(viewsets.ModelViewSet):
    queryset = OrderSummary.objects.all()
    serializer_class = OrderSummarySerializer

    def create(self, request, *args, **kwargs):
        logger.debug("Received data: %s", request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        chat_id = serializer.validated_data.get('chat_id')
        if not chat_id:
            logger.error("chat_id is missing in the request data.")
            return Response({"detail": "chat_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        chat_id = serializer.validated_data.get('chat_id')
        if not chat_id:
            logger.error("chat_id is missing in the request data.")
            return Response({"detail": "chat_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_update(serializer)
        
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        
        return Response(serializer.data)


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
        logger.info(f"Retrieve request received with phone: {phone} and chat_id: {chat_id}")
        if phone and chat_id:
            try:
                user = TelegramUser.objects.get(phone=phone, chat_id=chat_id)
                serializer = self.get_serializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except TelegramUser.DoesNotExist:
                return Response({"detail": "TelegramUser not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"detail": "Bad request. Phone and chat_id required."}, status=status.HTTP_400_BAD_REQUEST)


    def perform_create(self, serializer):
        telegram_user = serializer.save()
        orders = Order.objects.filter(phone=telegram_user.phone)
        for order in orders:
            if not order.telegram_user:  # Ensure only orders without an associated TelegramUser are updated
                order.telegram_user = telegram_user
                order.save(update_fields=['telegram_user'])
                self.stdout.write(f'Updated Order {order.id} with TelegramUser {telegram_user.id}\n')

    def perform_update(self, serializer):
        telegram_user = serializer.save()
        orders = Order.objects.filter(phone=telegram_user.phone)
        for order in orders:
            if not order.telegram_user:  # Ensure only orders without an associated TelegramUser are updated
                order.telegram_user = telegram_user
                order.save(update_fields=['telegram_user'])


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
            chat_id = data['message']['chat']['id']
            contact = data['message'].get('contact')

            if not contact:
                return JsonResponse({'status': 'error', 'message': 'No contact information'}, status=400)
            
            phone = contact.get('phone_number')
            if not phone:
                return JsonResponse({'status': 'error', 'message': 'No phone number in contact information'}, status=400)
            
            telegram_user, created = TelegramUser.objects.update_or_create(
                phone=phone, defaults={'chat_id': chat_id}
            )
            return JsonResponse({'status': 'ok'})
        except json.JSONDecodeError as e:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)
        except KeyError as e:
            return JsonResponse({'status': 'error', 'message': 'Missing required field'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'Internal server error'}, status=500)

telegram_webhook = TelegramWebhook.as_view()


@api_view(['POST'])
@permission_classes([AllowAny])
def create_order(request):
    logger.info(f"Order creation request data: {request.data}")

    try:
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            # Save the order first
            order = serializer.save()

            # Extract phone and get chat_id
            phone = request.data.get('phone')
            try:
                telegram_user = TelegramUser.objects.get(phone=phone)
                if telegram_user:
                    order.telegram_user = telegram_user
                    order.save(update_fields=['telegram_user'])

                    # Prepare order items
                    order_items = order.order_items.all()

                    # Notify the user about the new order status
                    update_order_status_with_notification(
                        order.id,
                        order_items,
                        'submitted',  # Assuming 'submitted' is the initial status
                        'submitted_at',
                        telegram_user.chat_id
                    )
                else:
                    logger.warning(f"No TelegramUser found with phone: {phone}")

            except TelegramUser.DoesNotExist:
                logger.warning(f"No TelegramUser found with phone: {phone}")


            # Send the confirmation email
            formatted_date = localtime(order.submitted_at).strftime('%Y-%m-%d %H:%M')
            order_items = order.order_items.all()
            total_sum = sum(item.quantity * item.product.price for item in order_items)
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

            email_body = f"""
            <html>
            <head>
                <style>
                    /* Add any CSS styling here */
                </style>
            </head>
            <body>
                <h2>Підтвердження замовлення #{order.id} на сайті KOLORYT</h2>
                {formatted_date}
                {order_items_table}
                <p><strong>Разом:</strong> {total_sum} {currency}</p>
                <p>Якщо у вас є питання, не вагайтеся зв'язатися з нами.</p>
                <p>З найкращими побажаннями,<br>
                Команда <a href='{settings.VERCEL_DOMAIN}'>KOLORYT</a></p>
                <p><a href='{settings.VERCEL_DOMAIN}'>Відмовитися від підписок</a></p>
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

            return Response({'status': 'Order created', 'order_id': order.id}, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"Order creation failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Order creation exception: {e}")
        return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order(request, order_id):
    """
    Retrieve a specific order by its ID.
    """
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
    """
    Retrieve all orders related to a specific Telegram user.
    """
    chat_id = request.query_params.get('chat_id', None)
    if not chat_id:
        return Response({'error': 'Chat ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        telegram_user = TelegramUser.objects.get(chat_id=chat_id)
        orders = Order.objects.filter(telegram_user=telegram_user)
        serializer = OrderSerializer(orders, many=True)
        return Response({'count': orders.count(), 'results': serializer.data}, status=status.HTTP_200_OK)
    except TelegramUser.DoesNotExist:
        return Response({'error': 'Telegram user not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error fetching orders: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
def update_order(request):
    chat_id = request.data.get('chat_id')
    orders = request.data.get('orders')

    if not chat_id:
        return Response({"detail": "chat_id is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        order_summary = OrderSummary.objects.get(chat_id=chat_id)
        order_summary.orders = orders
        order_summary.save()
        
        return Response({"message": "Order summary updated successfully."}, status=status.HTTP_200_OK)
    except OrderSummary.DoesNotExist:
        return Response({"error": "Order summary not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def get_order_summary_by_chat_id(request, chat_id):
    try:
        # Retrieve summaries by chat_id
        summaries = OrderSummary.objects.filter(chat_id=chat_id)
        if not summaries.exists():
            raise Http404('No summaries found for this chat ID.')

        summary_data = [
            {
                'chat_id': summary.chat_id,
                'orders': [
                    {
                        'order_id': order.order_id,
                        'order_items': [
                            {
                                'product_name': item.product_name,
                                'collection_name': item.collection_name,
                                'size': item.size,
                                'color_name': item.color_name,
                                'quantity': item.quantity,
                                'item_price': item.item_price,
                                'color_value': item.color_value
                            }
                            for item in order.order_items.all()
                        ],
                        'submitted_at': order.submitted_at,
                        'created_at': order.created_at,
                        'processed_at': order.processed_at,
                        'complete_at': order.complete_at,
                        'canceled_at': order.canceled_at
                    }
                    for order in summary.orders.all()
                ]
            }
            for summary in summaries
        ]

        return JsonResponse({'results': summary_data})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_summary(request):
    chat_id = request.query_params.get('chat_id')
    
    if not chat_id:
        return Response({'error': 'Chat ID is required.'}, status=400)

    try:
        summary = OrderSummary.objects.get(chat_id=chat_id)
        serializer = OrderSummarySerializer(summary)
        return Response(serializer.data)
    except OrderSummary.DoesNotExist:
        return Response({'error': 'No orders found for this chat ID.'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    

#@api_view(['POST'])
#@permission_classes([AllowAny])
#def update_order_summary(request):
#    chat_id = request.data.get('chat_id')
#    orders = request.data.get('orders', {})  # Ensure orders defaults to an empty dict

#    if not chat_id:
#        return Response({"detail": "chat_id is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Log the incoming data
#    logger.info(f"Updating OrderSummary: chat_id={chat_id}, orders={orders}")

#    try:
#        order_summary, created = OrderSummary.objects.get_or_create(chat_id=chat_id)
#        order_summary.orders = orders
#        order_summary.save()

#        return Response({"message": "Order summary updated successfully."}, status=status.HTTP_200_OK)
#    except Exception as e:
#        logger.error(f"Error updating OrderSummary: {e}")
#        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



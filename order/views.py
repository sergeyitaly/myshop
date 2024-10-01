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
import logging, requests, json
from django.http import JsonResponse
from rest_framework.decorators import action
from .notifications import update_order_status_with_notification
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils.dateformat import format as date_format
from django.utils.timezone import make_naive, is_aware
from datetime import datetime



logger = logging.getLogger(__name__)
def health_check(request):
    return JsonResponse({'status': 'ok'})

class OrderSummaryViewSet(viewsets.ModelViewSet):
    queryset = OrderSummary.objects.all()
    serializer_class = OrderSummarySerializer

    def format_timestamp(self, timestamp):
        # Format timestamp to 'Y-m-d H:i'
        return date_format(timestamp, 'Y-m-d H:i') if timestamp else None

    def make_aware_if_naive(self, dt):
        # Convert naive datetime to aware using Django's timezone support
        if dt and isinstance(dt, datetime):
            if timezone.is_naive(dt):
                return timezone.make_aware(dt)
        return dt

    def prepare_order_summary(self, order_summary):
        # Extracting order items and preparing summary
        order_items = [
            {
                "size": item.size,
                "quantity": item.quantity,
                "total_sum": item.total_sum,
                "color_name": item.color_name,
                "item_price": str(item.item_price),
                "color_value": item.color_value,
                "product_name": item.product_name,
                "collection_name": item.collection_name,
            }
            for item in order_summary.order.order_items.all()
        ]

        # Convert all relevant fields to timezone-aware datetimes
        order_created_at = self.make_aware_if_naive(order_summary.order.created_at)
        order_submitted_at = self.make_aware_if_naive(order_summary.order.submitted_at)
        order_processed_at = self.make_aware_if_naive(order_summary.order.processed_at)
        order_complete_at = self.make_aware_if_naive(order_summary.order.complete_at)
        order_canceled_at = self.make_aware_if_naive(order_summary.order.canceled_at)

        # Prepare summary with formatted timestamps
        order_summary_data = {
            "order_id": order_summary.order.id,
            "order_items": order_items,
            "created_at": self.format_timestamp(order_created_at),
            "submitted_at": self.format_timestamp(order_submitted_at),
            "processed_at": self.format_timestamp(order_processed_at),
            "complete_at": self.format_timestamp(order_complete_at),
            "canceled_at": self.format_timestamp(order_canceled_at)
        }

        # Only keep the latest timestamp status
        status_fields = ['submitted_at', 'created_at', 'processed_at', 'complete_at', 'canceled_at']
        latest_status = max(
            ((field, order_summary_data[field]) for field in status_fields if order_summary_data[field]),
            key=lambda x: self.make_aware_if_naive(x[1]),  # Ensure all compared fields are aware
            default=None
        )
        if latest_status:
            # Keep only the latest status in the response
            order_summary_data = {
                "order_id": order_summary.order.id,
                "order_items": order_items,
                latest_status[0]: latest_status[1],
            }

        return order_summary_data

    def create(self, request, *args, **kwargs):
        logger.debug("Received data: %s", request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        chat_id = serializer.validated_data.get('chat_id')
        if not chat_id:
            logger.error("chat_id is missing in the request data.")
            return Response({"detail": "chat_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Perform creation
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Prepare formatted order summary
        order_summary_data = self.prepare_order_summary(serializer.instance)
        
        return Response(order_summary_data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        chat_id = request.data.get('chat_id')
        if not chat_id:
            logger.error("chat_id is missing in the request data.")
            return Response({"detail": "chat_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate and update instance
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Handle potential prefetched objects cache
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        # Prepare updated order summary
        order_summary_data = self.prepare_order_summary(instance)

        return Response(order_summary_data)


    


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
    
def safe_make_naive(dt):
    if dt is None:
        return None
    return make_naive(dt) if is_aware(dt) else dt

def format_order_summary(order):
    submitted_at = safe_make_naive(order.submitted_at)
    processed_at = safe_make_naive(order.processed_at)
    complete_at = safe_make_naive(order.complete_at)
    canceled_at = safe_make_naive(order.canceled_at)

    statuses = {
        'submitted_at': submitted_at,
        'processed_at': processed_at,
        'complete_at': complete_at,
        'canceled_at': canceled_at
    }
    
    latest_status_field = max(
        statuses,
        key=lambda s: statuses[s] or datetime.min
    )
    latest_status_timestamp = statuses[latest_status_field]

    def datetime_to_str(dt):
        if dt:
            return dt.strftime('%Y-%m-%d %H:%M')
        return None

    serializer = OrderSerializer(order)
    order_data = serializer.data

    return {
        'order_id': order.id,
        'order_items': order_data['order_items'],
        'submitted_at': datetime_to_str(submitted_at),
        latest_status_field: datetime_to_str(latest_status_timestamp)
    }

@api_view(['POST'])
def update_order(request):
    chat_id = request.data.get('chat_id')
    orders = request.data.get('orders')

    if not chat_id:
        return Response({"detail": "chat_id is required."}, status=status.HTTP_400_BAD_REQUEST)

    if not isinstance(orders, list):
        return Response({"detail": "Orders must be a list."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Retrieve existing orders based on the incoming order data
        updated_orders = []
        for order_data in orders:
            order_id = order_data.get('order_id')
            if not order_id:
                return Response({"detail": "Order ID is required."}, status=status.HTTP_400_BAD_REQUEST)

            order = Order.objects.get(id=order_id)  # Adjust as needed based on your logic
            formatted_order = format_order_summary(order)
            updated_orders.append(formatted_order)

        # Update or create the OrderSummary with the formatted orders
        OrderSummary.objects.update_or_create(
            chat_id=chat_id,
            defaults={'orders': updated_orders}
        )

        return Response({"message": "Order summary updated successfully."}, status=status.HTTP_200_OK)

    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
    except OrderSummary.DoesNotExist:
        return Response({"error": "Order summary not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_summary_by_chat_id(request, chat_id):
    if not chat_id:
        return Response({'error': 'Chat ID is required.'}, status=400)

    try:
        summaries = OrderSummary.objects.filter(chat_id=chat_id)
        if not summaries.exists():
            return Response({'error': 'No summaries found for this chat ID.'}, status=404)
        summary_data = []
        for summary in summaries:
            orders = summary.orders 
            for order in orders:
                order_data = {
                    'order_id': order.get('order_id'),
                    'created_at': order.get('created_at'),
                    'submitted_at': order.get('submitted_at'),
                    'processed_at': order.get('processed_at'),
                    'complete_at': order.get('complete_at'),
                    'canceled_at': order.get('canceled_at'),
                    'order_items': [
                        {
                            'product_name': item.get('product_name'),
                            'collection_name': item.get('collection_name'),
                            'size': item.get('size'),
                            'color_name': item.get('color_name'),
                            'quantity': item.get('quantity'),
                            'total_sum': float(item.get('total_sum', 0)),  
                            'item_price': str(item.get('item_price', '0')),  
                            'color_value': item.get('color_value')
                        }
                        for item in order.get('order_items', [])
                    ]
                }
                summary_data.append(order_data)
        return Response({'results': summary_data})
    except Exception as e:
        return Response({'error': str(e)}, status=500)

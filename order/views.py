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
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
import logging, requests, json
from rest_framework.decorators import action
from .notifications import update_order_status_with_notification
from django.utils.timezone import make_naive, is_aware
from datetime import datetime
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView

logger = logging.getLogger(__name__)
def health_check(request):                                                                                                              
    return JsonResponse({'status': 'ok'})

def ensure_datetime(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        logger.error(f"Invalid datetime format: {value}")
        return None

def format_timestamp(timestamp):
    return timestamp.strftime('%Y-%m-%d %H:%M') if timestamp else None

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
        order_summary_data = format_order_summary(serializer.instance)  # Directly call the updated method
        return Response(order_summary_data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        chat_id = request.data.get('chat_id')
        if not chat_id:
            logger.error("chat_id is missing in the request data.")
            return Response({"detail": "chat_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Refresh the instance to reload any related fields if necessary
        instance.refresh_from_db()

        # Prepare the updated order summary data
        order_summary_data = format_order_summary(instance)  # Directly call the updated method
        return Response(order_summary_data)


class TelegramUserViewSet(viewsets.ModelViewSet):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [TokenAuthentication]

    @action(detail=False, methods=['get'], url_path='by-phone')
    def get_by_phone(self, request):
        phone = request.query_params.get('phone')
        if phone:
            try:
                user = TelegramUser.objects.get(phone=phone)
                serializer = self.get_serializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except TelegramUser.DoesNotExist:
                return Response({"detail": "TelegramUser not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"detail": "Phone parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

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

class TelegramMessageListCreateView(ListCreateAPIView):
    queryset = TelegramMessage.objects.all()
    serializer_class = TelegramMessageSerializer

class TelegramMessageDetailView(RetrieveAPIView):
    queryset = TelegramMessage.objects.all()
    serializer_class = TelegramMessageSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated] 

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
    webhook_url = f"{settings.VERCEL_DOMAIN}/api/telegram_webhook/"  
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




def calculate_popularity(sales_count, stock):
    max_sales_count = 1000
    max_stock = 100
    sales_popularity = min(10, (sales_count / max_sales_count) * 10)
    stock_popularity = min(10, (stock / max_stock) * 10)
    popularity = int((sales_popularity + stock_popularity) / 2)
    return max(1, min(10, popularity))


@api_view(['POST'])
@permission_classes([AllowAny])
def create_order(request):
    try:
        serializer = OrderSerializer(data=request.data)
        language = request.data.get('language')
        order_data = request.data.copy()
        order_data['language'] = language   
  
        if serializer.is_valid():
            order = serializer.save()
            phone = request.data.get('phone')
            order_items_en = serializer.get_order_items_en(order)
            order_items_uk = serializer.get_order_items_uk(order)

            for item_data in request.data.get('order_items', []):
                product_id = item_data.get('product_id')
                quantity = item_data.get('quantity')
                if not product_id:
                    raise ValidationError("product_id is required for order items.")

                try:
                    product = Product.objects.get(id=product_id)
                except Product.DoesNotExist:
                    raise ValidationError(f"Product with id {product_id} does not exist.")

                # Update product fields
                product.sales_count += quantity
                product.stock -= quantity
                if product.stock <=0:
                    product.available = False
                product.popularity = calculate_popularity(product.sales_count, product.stock)
                product.save()

            try:
                telegram_user = TelegramUser.objects.get(phone=phone)
                if telegram_user:
                    order.telegram_user = telegram_user
                    order.save(update_fields=['telegram_user'])
                    order_items = order.order_items.all()
                    update_order_status_with_notification(
                        order.id,
                        order_items,
                        'submitted',
                        'submitted_at',
                        telegram_user.chat_id,
                        language
                    )
                else:
                    logger.warning(f"No TelegramUser found with phone: {phone}")

            except TelegramUser.DoesNotExist:
                logger.warning(f"No TelegramUser found with phone: {phone}")

            formatted_date = localtime(order.submitted_at).strftime('%Y-%m-%d %H:%M')


            def generate_order_items_en_table(order_items):
                return "".join([
                    f"""
                    <tr>
                        <td>{index + 1}</td>
                        <td><img src="{item['product']['photo']}" alt="{item['product']['name_en']}" style="width: 50px; height: 50px; object-fit: cover;" /></td>
                        <td>{item['product']['name_en']}</td>
                        <td>{item['product']['collection']['name_en']}</td>
                        <td>{item['quantity']}</td>
                        <td>{item['product']['size']}</td>
                        <td>{item['product']['color_name_en']}<br> <div style="width: 10px; height: 10px; background-color: {item['product']['color_value']}; display: inline-block;"></div></td>
                        <td>{item['product']['price']} {item['product']['currency']}</td>
                    </tr>
                    """
                    for index, item in enumerate(order_items)
                ])
            def generate_order_items_uk_table(order_items):
                return "".join([
                    f"""
                    <tr>
                        <td>{index + 1}</td>
                        <td><img src="{item['product']['photo']}" alt="{item['product']['name_uk']}" style="width: 50px; height: 50px; object-fit: cover;" /></td>
                        <td>{item['product']['name_uk']}</td>
                        <td>{item['product']['collection']['name_uk']}</td>
                        <td>{item['quantity']}</td>
                        <td>{item['product']['size']}</td>
                        <td>{item['product']['color_name_uk']}<br> <div style="width: 10px; height: 10px; background-color: {item['product']['color_value']}; display: inline-block;"></div></td>
                        <td>{item['product']['price']} {item['product']['currency']}</td>
                    </tr>
                    """
                    for index, item in enumerate(order_items)
                ])
            email_body_en = f"""
            <html>
            <head>
                <style>
                    /* Add any CSS styling here */
                </style>
            </head>
            <body>
                <h2>Order Confirmation #{order.id} from KOLORYT</h2>
                <p>Order Date: {formatted_date}</p>
                <h3>Items in the order: </h3>
                <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">
                    <thead>
                        <tr>
                            <th>No</th>
                            <th>Photo</th>
                            <th>Product Name</th>
                            <th>Collection</th>
                            <th>Quantity</th>
                            <th>Size</th>
                            <th>Color</th>
                            <th>Price</th>
                        </tr>
                    </thead>
                    <tbody>
                        {generate_order_items_en_table(order_items_en)}
                    </tbody>
                </table>
                <p><strong>Total:</strong> {sum(item['total_sum'] for item in order_items_en)} {order_items_en[0]['product']['currency'] if order_items_en else 'USD'}</p>
                <p>If you have any questions, feel free to contact us.</p>
                <p>Best regards,<br>
                KOLORYT Team <a href='{settings.VERCEL_DOMAIN}'>KOLORYT</a></p>
                <p><a href='{settings.VERCEL_DOMAIN}'>Unsubscribe</a></p>
            </body>
            </html>
            """
            email_body_uk = f"""
            <html>
            <head>
                <style>
                    /* Add any CSS styling here */
                </style>
            </head>
            <body>
                <h2>Підтвердження замовлення #{order.id} на сайті KOLORYT</h2>
                <p>Дата замовлення: {formatted_date}</p>
                <h3>Продукти в замовленні: </h3>
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
                        {generate_order_items_uk_table(order_items_uk)}
                    </tbody>
                </table>
                <p><strong>Разом:</strong> {sum(item['total_sum'] for item in order_items_uk)} {order_items_uk[0]['product']['currency'] if order_items_uk else 'UAH'}</p>
                <p>Якщо у вас є питання, не вагайтеся зв'язатися з нами.</p>
                <p>З найкращими побажаннями,<br>
                Команда <a href='{settings.VERCEL_DOMAIN}'>KOLORYT</a></p>
                <p><a href='{settings.VERCEL_DOMAIN}'>Відмовитися від підписок</a></p>
            </body>
            </html>
            """
            if language == 'en':
                email_body = email_body_en
                email = EmailMessage(
                subject=f'Order Confirmation #{order.id}',
                body=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[order.email],
                headers={'Content-Type': 'text/html; charset=utf-8'}
                 )
            else:
                email_body = email_body_uk
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

def safe_make_naive(timestamp):
    if isinstance(timestamp, str):
        try:
            timestamp = datetime.fromisoformat(timestamp)  # Parse string to datetime
        except ValueError:
            logger.error(f"Invalid timestamp format: {timestamp}")
            return None
    if timestamp is not None and is_aware(timestamp):
        return make_naive(timestamp)
    elif timestamp is not None and not is_aware(timestamp):
        return timestamp
    return None

def format_order_summary(order):
    statuses = {
        'submitted_at': safe_make_naive(order.submitted_at),
        'created_at': safe_make_naive(order.created_at),
        'processed_at': safe_make_naive(order.processed_at),
        'complete_at': safe_make_naive(order.complete_at),
        'canceled_at': safe_make_naive(order.canceled_at),
    }
    latest_status_field = max(
        statuses, key=lambda s: statuses[s] or datetime.min
    )
    latest_status_timestamp = statuses[latest_status_field]
    order_items_en = []
    order_items_uk = []
    for item in order.order_items.all():
        product = item.product
        order_items_en.append({
            'name': product.name_en,
            'size': product.size,
            'price': float(product.price),
            'currency': product.currency,
            'quantity': item.quantity,
            'color_name': product.color_name_en,
            'color_value': product.color_value,
            'collection_name': product.collection.name_en if product.collection else 'No Collection',
        })
        order_items_uk.append({
            'name': product.name_uk,
            'size': product.size,
            'price': float(product.price),
            'currency': product.currency,
            'quantity': item.quantity,
            'color_name': product.color_name_uk,
            'color_value': product.color_value,
            'collection_name': product.collection.name_uk if product.collection else 'No Collection',
        })
    return {
        'order_id': order.id,
        'submitted_at': format_timestamp(statuses['submitted_at']),
        latest_status_field: format_timestamp(latest_status_timestamp),
        'order_items_en': order_items_en,
        'order_items_uk': order_items_uk,
    }


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_summary_by_chat_id(request, chat_id):
    if not chat_id:
        return Response({'error': 'Chat ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        summaries = OrderSummary.objects.filter(chat_id=chat_id)
        if not summaries.exists():
            return Response({'error': 'No summaries found for this chat ID.'}, status=status.HTTP_404_NOT_FOUND)

        summary_data = []
        for summary in summaries:
            orders = summary.orders
            for order in orders:
                status_timestamps = {
                    'created_at': safe_make_naive(order.get('created_at')),
                    'submitted_at': safe_make_naive(order.get('submitted_at')),
                    'processed_at': safe_make_naive(order.get('processed_at')),
                    'complete_at': safe_make_naive(order.get('complete_at')),
                    'canceled_at': safe_make_naive(order.get('canceled_at')),
                }
                latest_status_timestamp = max(
                    (timestamp for timestamp in status_timestamps.values() if timestamp is not None),
                    default=None
                )
                latest_status_field = next(
                    (field for field, timestamp in status_timestamps.items() if timestamp == latest_status_timestamp),
                    None
                )
                order_data = {
                    'order_id': order.get('order_id'),
                    'order_items_en': order.get('order_items_en', []),
                    'order_items_uk': order.get('order_items_uk', []),
                    'submitted_at': status_timestamps['submitted_at'].isoformat() if status_timestamps['submitted_at'] else None,
                    latest_status_field: latest_status_timestamp.isoformat() if latest_status_timestamp else None
                }
                summary_data.append(order_data)
        logger.debug(f"Order summary response: {summary_data}")
        return Response({'results': summary_data}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching order summaries: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
def update_order(request):
    chat_id = request.data.get('chat_id')
    orders = request.data.get('orders', [])
    
    # Validate the input
    if not chat_id:
        return Response({"detail": "chat_id is required."}, status=status.HTTP_400_BAD_REQUEST)
    if not isinstance(orders, list):
        return Response({"detail": "Orders must be a list."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        grouped_orders = []
        for order_data in orders:
            order_id = order_data.get('order_id')
            language = order_data.get('language')
            if not order_id:
                return Response({"detail": "Order ID is required for each order."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                order = Order.objects.prefetch_related('order_items__product').get(id=order_id)
                if language:
                    order.language = language 
                order.save()

                # Update product availability based on stock
                for order_item in order.order_items.all():
                    product = order_item.product
                    if product.stock <= 0:
                        product.available = False
                        product.save()

                order_summary = format_order_summary(order)
                grouped_orders.append(order_summary)

            except Order.DoesNotExist:
                return Response({"error": f"Order with ID {order_id} not found."}, status=status.HTTP_404_NOT_FOUND)
        
        OrderSummary.objects.update_or_create(
            chat_id=chat_id,
            defaults={'orders': grouped_orders},
        )
        
        return Response({"message": "Order summary updated successfully."}, status=status.HTTP_200_OK)
    
    except Exception as e:
        logger.error(f"Error updating order summary: {e}")
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

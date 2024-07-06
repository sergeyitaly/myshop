from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.mail import send_mail
from .models import Order, OrderItem, Product
from .serializers import OrderSerializer, OrderItemSerializer
from django.conf import settings

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def create_order(request):
    print("Received data:", request.data)  # Debugging line to print the incoming data
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        order = serializer.save()
        try:
            order_items_info = "\n".join(
                [f"{item.quantity} of {Product.objects.get(id=item.product_id).name}" for item in order.order_items.all()]
            )
            send_mail(
                'Order Confirmation',
                f'Thank you for your order, {order.name}!\n\nYour order details:\n\n{order_items_info}',
                settings.EMAIL_HOST_USER,  # Use default sender email from settings
                [order.email],
            )
        except Exception as e:
            print(f'Error sending email: {e}')
            # You can choose to handle the exception here, e.g., log it or return an error response
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print("Validation Errors:", serializer.errors)  # Debugging line to print validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def send_email(request):
    try:
        to_email = request.data.get('to')
        subject = request.data.get('subject')
        body = request.data.get('body')
        sender_email = settings.EMAIL_HOST_USER  # Use default sender email from settings

        if not to_email or not subject or not body:
            return Response(
                {'message': 'To, subject, and body fields are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        send_mail(subject, body, sender_email, [to_email])

        return Response({'message': 'Email sent successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        print(f'Error sending email: {e}')
        return Response({'message': f'Error sending email: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

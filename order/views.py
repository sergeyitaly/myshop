from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from .serializers import OrderSerializer
from .models import Order, OrderItem

@api_view(['POST'])
@permission_classes([AllowAny])  # Allow anonymous access
def create_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        order = serializer.save()
        try:
            send_mail(
                'Order Confirmation',
                f'Thank you for your order, {order.name}!\n\nYour order details:\n\n{serializer.data}',
                'your_email@example.com',
                [order.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f'Error sending email: {e}')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

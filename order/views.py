from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from .utils import send_mailgun_email
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
    print("MAILGUN_API_KEY:", settings.MAILGUN_API_KEY)  # Debugging line to print the API key
    print("MAILGUN_DOMAIN:", settings.MAILGUN_DOMAIN)  # Debugging line to print the domain
    print("DEFAULT_FROM_EMAIL:", settings.DEFAULT_FROM_EMAIL)  # Debugging line to print the from email
    
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        order = serializer.save()
        try:
            order_items_info = "\n".join(
                [f"{item['quantity']} of product ID {item['product_id']}" for item in request.data['order_items']]
            )
            response = send_mailgun_email(
                order.email,
                'Order Confirmation',
                f'Thank you for your order, {order.name}!\n\nYour order details:\n\n{order_items_info}'
            )
            if response.status_code == 200:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print(f'Error sending email: {response.text}')
                return Response({'message': f'Error sending email: {response.text}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(f'Error sending email: {e}')
            return Response({'message': f'Error sending email: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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

        if not to_email or not subject or not body:
            return Response(
                {'message': 'To, subject, and body fields are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        response = send_mailgun_email(to_email, subject, body)
        if response.status_code == 200:
            return Response({'message': 'Email sent successfully'}, status=status.HTTP_200_OK)
        else:
            print(f'Error sending email: {response.text}')
            return Response({'message': f'Error sending email: {response.text}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        print(f'Error sending email: {e}')
        return Response({'message': f'Error sending email: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

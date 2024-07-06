from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.mail import send_mail
from .models import Order, OrderItem, Product
from .serializers import OrderSerializer, OrderItemSerializer

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
                'your_email@example.com',
                [order.email],
            )
        except Exception as e:
            print(f'Error sending email: {e}')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print("Validation Errors:", serializer.errors)  # Debugging line to print validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])  # Allow anonymous access
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

        # Assuming sender_email is provided in your request data or you retrieve it from somewhere else
        sender_email = request.data.get('sender_email', 'your_email@example.com')

        send_mail(subject, body, sender_email, [to_email])

        return Response({'message': 'Email sent successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        print(f'Error sending email: {e}')
        return Response({'message': f'Error sending email: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

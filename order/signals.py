# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, OrderSummary

@receiver(post_save, sender=Order)
def update_order_summary(sender, instance, **kwargs):
    chat_id = instance.telegram_user.chat_id if instance.telegram_user else None
    if chat_id:
        order_summary, created = OrderSummary.objects.get_or_create(chat_id=chat_id)
        orders = [order.to_summary_dict() for order in Order.objects.filter(telegram_user__chat_id=chat_id)]
        order_summary.orders = orders
        order_summary.save()

from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# models for which notifications are sent
from products.models import Product


@receiver(post_save, sender=Product)
def notify_on_new_product(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        message = f'New product added: {instance.name}'

        async_to_sync(channel_layer.group_send)(
            'global_notifications',
            {
                'type': 'send_notification',
                'type_notification': 'new_product',
                'message': message,
                'sender': sender
            }
        )


# @receiver(post_save, sender=Product)
def notify_on_product_update(sender, instance, **kwargs):
    # if not created:
    channel_layer = get_channel_layer()
    message = f'Product updated: {instance.name}'

    async_to_sync(channel_layer.group_send)(
        'global_notifications',
        {
            'type': 'send_notification',
            'type_notification': 'update_product',
            'message': message,
            'sender': sender
        }
    )

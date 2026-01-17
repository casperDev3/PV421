from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import News


@receiver(post_save, sender=News)
def send_news_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "interactive_room",
            {
                "type": "broadcast_news",  # Це ім'я методу, який треба додати в Consumer
                "title": instance.title,
                "image": instance.image_url if instance.image_url else "",
                "message": " 🔥 Гаряча новина!"
            }
        )
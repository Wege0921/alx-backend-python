from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        return  # Skip if it's a new message

    try:
        old_instance = Message.objects.get(pk=instance.pk)
        if old_instance.content != instance.content:
            MessageHistory.objects.create(
                message=old_instance,
                old_content=old_instance.content
            )
            instance.edited = True  # Mark as edited
    except Message.DoesNotExist:
        pass


from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import MessageHistory, Message

@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    # Cleanup MessageHistory records where user was sender or receiver
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()

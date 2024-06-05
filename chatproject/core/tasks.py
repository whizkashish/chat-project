# core/tasks.py

from celery import shared_task
from .models import Notifications

@shared_task
def test_task():
    return "Celery is working!"

@shared_task
def mark_notifications_as_read(user_id, room_id):
    Notifications.objects.filter(user_id=user_id, room_id=room_id, is_read=False).update(is_read=True)

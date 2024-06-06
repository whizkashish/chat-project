# chat/models.py
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import uuid

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)

    class Meta:
        abstract = True

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    @property
    def is_deleted(self):
        return self.deleted_at is not None

class ChatRoom(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_chat_rooms')
    is_group = models.BooleanField(default=False)

class ChatRoomUser(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(timezone.now())

    class Meta:
        unique_together = ('user', 'chatroom')

class Message(TimestampedModel):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f'{self.user.username}: {self.content}'

class Profile(TimestampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    @property
    def is_complete(self):
        # Define your logic to check if the profile is complete
        return bool(self.date_of_birth and self.gender and self.address and self.zip_code and self.image)

class Notifications(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications',null=True)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, null=True)
    content = models.TextField(null=True)
    is_read = models.BooleanField(default=False)

class Membership(TimestampedModel):
    MEMBERSHIP_CHOICES = (
        ('Free', 'free'),
        ('Pro', 'pro'),
        ('Premium', 'premium'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=40, default=False)
    stripe_subscription_id = models.CharField(max_length=40, default=False)
    membership_type = models.CharField(max_length=30, choices=MEMBERSHIP_CHOICES, default='Free')
    start_date = models.DateTimeField(default = timezone.now())
    end_date = models.DateTimeField(default= datetime.now() + timedelta(days=1))
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
    
class MembershipPayment(TimestampedModel):
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.membership.user.username} - {self.amount} - {self.payment_date}"
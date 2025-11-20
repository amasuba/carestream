from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)

class SessionData(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    qoe_score = models.FloatField(default=5.0)
    status = models.CharField(max_length=20, default="active")


class Ticket(models.Model):
    session = models.ForeignKey(SessionData, on_delete=models.CASCADE, related_name='tickets')
    title = models.CharField(max_length=256)
    priority = models.CharField(max_length=32, default='MEDIUM')
    assigned_to = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)


class Notification(models.Model):
    session = models.ForeignKey(SessionData, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=32, default='sms_app')
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
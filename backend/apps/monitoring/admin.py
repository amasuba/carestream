from django.contrib import admin
from .models import Customer, SessionData, Ticket, Notification


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email')


@admin.register(SessionData)
class SessionDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'start_time', 'end_time', 'qoe_score', 'status')
    list_filter = ('status',)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'title', 'priority', 'assigned_to', 'created_at', 'resolved')
    list_filter = ('priority', 'resolved')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'type', 'sent_at')
    list_filter = ('type',)
from django.contrib import admin

# Register your models here.

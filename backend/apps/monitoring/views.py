import threading
import time
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Customer, SessionData, Ticket, Notification
import requests


def _local_predict(session):
    """Fallback local ML predictor: returns (score, confidence)."""
    # Simulate a heavier ML call but fast: produce a low QoE for demo
    score = round(random.uniform(1.8, 2.4), 2)
    confidence = 0.89
    return score, confidence

# In-memory helper to keep track of running simulation thread and state id
_sim = {
    'thread': None,
    'running': False,
    'current_step': 0,
}

def _ensure_customer(name="Customer_JHB", location="JOHANNESBURG"):
    customer, _ = Customer.objects.get_or_create(name=name, defaults={"phone": "", "email": ""})
    return customer

def _create_session(customer):
    session = SessionData.objects.create(customer=customer, qoe_score=5.0, status='idle')
    return session

def _simulate(session_id):
    """Simulate the scenario and update the SessionData record over time."""
    steps = [
        ("Detection", 2),
        ("Prediction", 2),
        ("Ticket Creation", 1),
        ("Customer Notification", 1),
        ("Resolution", 2),
        ("Follow-up & Feedback", 1),
    ]

    _sim['running'] = True
    for idx, (name, duration) in enumerate(steps, start=1):
        _sim['current_step'] = idx
        try:
            session = SessionData.objects.get(id=session_id)
        except SessionData.DoesNotExist:
            break

        if name == 'Detection':
            session.status = 'degraded'
            session.qoe_score = 3.5
            session.save()
        elif name == 'Prediction':
            # Try calling external ML predictor service; fall back to local simulation
            try:
                resp = requests.post('http://127.0.0.1:8002/predict', json={'session_id': session.id}, timeout=1.0)
                if resp.status_code == 200:
                    data = resp.json()
                    score = float(data.get('qoe_score', 2.1))
                else:
                    score, conf = _local_predict(session)
            except Exception:
                # fallback simulated prediction using local predictor
                score, conf = _local_predict(session)

            session.qoe_score = score
            session.status = 'investigating'
            session.save()
        elif name == 'Ticket Creation':
            # Persist a ticket row
            ticket = Ticket.objects.create(
                session=session,
                title='Network latency issue in JHB region, customer streaming video',
                priority='HIGH',
                assigned_to='NETWORK OPS TEAM'
            )
            session.status = f'ticket_created:{ticket.priority}:{ticket.assigned_to}'
            session.save()
        elif name == 'Customer Notification':
            # create notification and mark sent
            notif = Notification.objects.create(
                session=session,
                type='sms_app',
                message="We detected an issue with your video service. Our network team is working on it. ETA: 5 minutes."
            )
            session.status = 'customer_notified'
            session.save()
        elif name == 'Resolution':
            session.qoe_score = 3.8
            session.status = 'ok'
            session.save()
        elif name == 'Follow-up & Feedback':
            notif = Notification.objects.create(
                session=session,
                type='sms_app',
                message="Issue resolved. Your service is back to normal. Please rate us."
            )
            session.status = 'followup_sent'
            session.save()

        time.sleep(duration)

    _sim['running'] = False
    _sim['current_step'] = len(steps)


def sessions_list(request):
    # Return latest session(s)
    sessions = SessionData.objects.select_related('customer').all().order_by('-start_time')[:10]
    out = []
    for s in sessions:
        out.append({
            'id': s.id,
            'customer': s.customer.name,
            'start_time': s.start_time.isoformat() if s.start_time else None,
            'end_time': s.end_time.isoformat() if s.end_time else None,
            'qoe_score': s.qoe_score,
            'status': s.status,
        })
    return JsonResponse(out, safe=False)


@csrf_exempt
def start_scenario(request):
    # Start a demo session and run the simulation in background
    customer = _ensure_customer()
    session = _create_session(customer)

    if _sim['running']:
        return JsonResponse({'started': False, 'reason': 'already running'})

    t = threading.Thread(target=_simulate, args=(session.id,), daemon=True)
    _sim['thread'] = t
    t.start()
    return JsonResponse({'started': True, 'session_id': session.id})


def scenario_state(request):
    # Return current simulation state and latest session
    latest = SessionData.objects.select_related('customer').order_by('-start_time').first()
    session_data = None
    if latest:
        session_data = {
            'id': latest.id,
            'customer': latest.customer.name,
            'qoe_score': latest.qoe_score,
            'status': latest.status,
        }

    # add ticket(s) and notifications to the response for the latest session
    tickets = []
    notifications = []
    if latest:
        for t in latest.tickets.all():
            tickets.append({
                'id': t.id,
                'title': t.title,
                'priority': t.priority,
                'assigned_to': t.assigned_to,
                'created_at': t.created_at.isoformat(),
                'resolved': t.resolved,
            })
        for n in latest.notifications.all():
            notifications.append({
                'id': n.id,
                'type': n.type,
                'message': n.message,
                'sent_at': n.sent_at.isoformat(),
            })

    return JsonResponse({
        'running': _sim['running'],
        'current_step': _sim['current_step'],
        'session': session_data,
        'tickets': tickets,
        'notifications': notifications,
    })
from django.shortcuts import render

# Create your views here.

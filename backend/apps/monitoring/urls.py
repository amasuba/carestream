from django.urls import path
from . import views

urlpatterns = [
    path('sessions/', views.sessions_list, name='sessions_list'),
    path('scenario/start', views.start_scenario, name='start_scenario'),
    path('scenario/state', views.scenario_state, name='scenario_state'),
]

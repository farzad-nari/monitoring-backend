from django.urls import path
from .views import ActiveAlertsView, AlertHistoryView, AlertAcknowledgeView


urlpatterns = [
    path('active/', ActiveAlertsView.as_view(), name='active-alerts'),
    path('history/', AlertHistoryView.as_view(), name='alert-history'),
    path('<int:pk>/acknowledge/', AlertAcknowledgeView.as_view(), name='acknowledge-alert')
]
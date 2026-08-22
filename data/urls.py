from django.urls import path
from .views import RealtimeView, TimeSeriesView


urlpatterns = [
    path('realtime/', RealtimeView.as_view(), name='realtime'),
    path('timeseries/', TimeSeriesView.as_view(), name='timeseries'),
]

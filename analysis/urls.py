from django.urls import path
from .views import ForecastView, AnomaliesView, RiskView, DecisionsView


urlpatterns = [
    path('forecast/', ForecastView.as_view(), name='forecast'),
    path('anomalies/', AnomaliesView.as_view(), name='anomalies'),
    path('risk/', RiskView.as_view(), name='risk'),
    path('decisions/', DecisionsView.as_view(), name='decisions')
]


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Alert
from .serializers import AlertSerializer


class ActiveAlertsView(APIView):
    def get(self, request):
        alerts = Alert.objects.filter(is_active=True)

        if not alerts.exists():
            return Response({'message': 'no data available'}, status=204)

        serializer = AlertSerializer(alerts, many=True)
        return Response(serializer.data)


class AlertHistoryView(APIView):
    def get(self, request):
        alerts = Alert.objects.order_by('-created_at')[:100]

        if not alerts.exists():
            return Response({'message': 'no data available'}, status=204)

        serializer = AlertSerializer(alerts, many=True)
        return Response(serializer.data)


class AlertAcknowledgeView(APIView):
    def post(self, request, pk):
        try:
            alert = Alert.objects.get(pk=pk)

        except Alert.DoesNotExist:
            return Response({'error': 'alert not found'}, status=404)

        alert.is_acknowledged = True
        alert.acknowledged_at = timezone.now()

        if request.user.is_authenticated:
            alert.acknowledged_by = request.user
            
        alert.save()

        return Response({'status': 'acknowledged'})



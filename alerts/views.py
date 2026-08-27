from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Alert
from .serializers import AlertSerializer
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse,
)
from drf_spectacular.types import OpenApiTypes
from rest_framework.permissions import IsAuthenticated


class ActiveAlertsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
            tags=['alerts'],
            summary='Get Active Alerts',
            description='Returns active alerts.',
            responses={
                200: OpenApiResponse(
                    description='Successful response',
                    response={
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                        'id': {'type': 'integer'},
                        'severity': {'type': 'string'},
                        'param': {'type': 'string'},
                        'message': {'type': 'string'},
                        'actual_value': {'type': 'number'},
                        'threshold_value': {'type': 'number'},
                        'unit_id': {'type': 'string'},
                        'is_active': {'type': 'boolean'},
                        'is_acknowledged': {'type': 'boolean'},
                        'acknowledged_at': {'type': 'string', 'format': 'date-time'},
                        'created_at': {'type': 'string', 'format': 'date-time'},
                        },
                    }
                },
                examples=[
                    OpenApiExample(
                        'Active alerts example',
                        value=[
                            {
                                'id': 2,
                                'severity': 'warning',
                                'param': 'param1',
                                'message': 'Test alert - temperature high',
                                'actual_value': 75.5,
                                'threshold_value': 70.0,
                                'unit_id': None,
                                'is_active': True,
                                'is_acknowledged': False,
                                'acknowledged_at': None,
                                'created_at': '2026-08-22T22:06:19Z',
                            }
                        ]
                    )
                ]
                ),
                204: OpenApiResponse(description='No active alerts')
            }
    )
    def get(self, request):
        alerts = Alert.objects.filter(is_active=True)

        if not alerts.exists():
            return Response({'message': 'no data available'}, status=204)

        serializer = AlertSerializer(alerts, many=True)
        return Response(serializer.data)


class AlertHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['alerts'],
        summary='Get Alert History',
        description='Returns alert history ordered by creation date.',
        responses={
            200: OpenApiResponse(
                description='Successful response',
                response={
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'severity': {'type': 'string'},
                            'param': {'type': 'string'},
                            'message': {'type': 'string'},
                            'actual_value': {'type': 'number'},
                            'threshold_value': {'type': 'number'},
                            'unit_id': {'type': 'string'},
                            'is_active': {'type': 'boolean'},
                            'is_acknowledged': {'type': 'boolean'},
                            'acknowledged_at': {'type': 'string', 'format': 'date-time'},
                            'created_at': {'type': 'string', 'format': 'date-time'},
                        }
                    }
                },
                examples=[
                    OpenApiExample(
                        'Alert history example',
                        value=[
                            {
                                'id': 5,
                                'severity': 'critical',
                                'param': 'param1',
                                'message': 'Temperature too high',
                                'actual_value': 95.3,
                                'threshold_value': 80.0,
                                'unit_id': 'unit-3',
                                'is_active': False,
                                'is_acknowledged': True,
                                'acknowledged_at': '2026-08-20T10:00:00Z',
                                'created_at': '2026-08-20T09:45:00Z',
                            },
                            {
                                'id': 4,
                                'severity': 'warning',
                                'param': 'param2',
                                'message': 'Pressure abnormal',
                                'actual_value': 45.7,
                                'threshold_value': 60.0,
                                'unit_id': None,
                                'is_active': True,
                                'is_acknowledged': False,
                                'acknowledged_at': None,
                                'created_at': '2026-08-19T15:20:00Z',
                            }
                        ]
                    )
                ]
            ),
            204: OpenApiResponse(description='No alerts found')
        }
    )
    def get(self, request):
        alerts = Alert.objects.order_by('-created_at')[:100]

        if not alerts.exists():
            return Response({'message': 'no data available'}, status=204)

        serializer = AlertSerializer(alerts, many=True)
        return Response(serializer.data)


class AlertAcknowledgeView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
            tags=['alerts'],
            summary='Acknowledge Alert',
            description='Acknowledges an alert by its ID.',
            parameters=[OpenApiParameter(
                name='id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='Alert ID',
                required=True,
            )
            ],
            responses={
                200: OpenApiResponse(
                    description='Alert acknowledged',
                    response={
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'}
                        }
                    },
                    examples=[
                        OpenApiExample(
                        'Success example',
                        value={
                            'status':'acknowledged',
                        }
                    )
                    ]
                ),
                404: OpenApiResponse(description='Alert not found'),
            }
    )
    def post(self, request, pk):
        try:
            alert = Alert.objects.get(pk=pk)

        except Alert.DoesNotExist:
            return Response({'error': 'alert not found'}, status=404)

        alert.is_acknowledged = True
        alert.acknowledged_at = timezone.now()
        alert.acknowledged_by = request.user
            
        alert.save()

        return Response({'status': 'acknowledged'})



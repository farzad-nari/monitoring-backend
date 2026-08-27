from rest_framework.views import APIView
from rest_framework.response import Response
from .models import AnalysisResult
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
)
from rest_framework.permissions import IsAuthenticated


class ForecastView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        tags=['analysis'],
        summary='Get Forecast',
        description='Returns the latest forecast from ML analysis.',
        responses={
            200: OpenApiResponse(
                description='Successful response',
                response={
                    'type': 'object',
                    'properties': {
                        'forecast': {
                            'type': 'object',
                            'properties': {
                                'param1_next_1h': {'type': 'number'},
                                'param1_next_6h': {
                                    'type': 'array',
                                    'items': {'type': 'number'},
                                },
                                'confidence': {'type': 'number'},
                                'mape': {'type': 'number'},
                            }
                        }
                    }
                },
                examples=[
                    OpenApiExample(
                        'Forecast example',
                        value={
                            'forecast': {
                                'param1_next_1h': 248.2,
                                'param1_next_6h': [245.1, 251.3, 255.6, 252.1, 248.8, 244.3],
                                'confidence': 0.87,
                                'mape': 3.2,
                            }
                        }
                    )
                ]
            ),
            204: OpenApiResponse(description='No data available'),
        }
    )
    def get(self, request):
        result = AnalysisResult.objects.order_by('-created_at').first()

        if not result or not result.forecast:
            return Response({'message': 'no data available'}, status=204)

        return Response({'forecast': result.forecast})


class AnomaliesView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['analysis'],
        summary='Get Anomalies',
        description='Returns the latest anomalies from ML analysis.',
        responses={
            200: OpenApiResponse(
                description='Successful response',
                response={
                    'type': 'object',
                    'properties': {
                        'anomalies': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'type': {'type': 'string'},
                                    'param': {'type': 'string'},
                                    'severity': {'type': 'string'},
                                    'unit_id': {'type': 'string'},
                                    'description': {'type': 'string'},
                                    'score': {'type': 'number'},
                                }
                            }
                        }
                    }
                },
                examples=[
                    OpenApiExample(
                        'Anomalies example',
                        value={
                            'anomalies': [
                                {
                                    'type': 'param_anomaly',
                                    'param': 'param2',
                                    'severity': 'high',
                                    'unit_id': 'unit-12',
                                    'description': 'Abnormal behavior detected',
                                    'score': 0.82,
                                }
                            ]
                        }
                    )
                ]
            ),
            204: OpenApiResponse(description='No data available'),
        }
    )
    def get(self, request):
        result = AnalysisResult.objects.order_by('-created_at').first()

        if not result or not result.anomalies:
            return Response({'message': 'no data available'}, status=204)

        return Response({'anomalies': result.anomalies})


class RiskView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['analysis'],
        summary='Get Risk Score',
        description='Returns the latest risk score and breakdown from ML analysis.',
        responses={
            200: OpenApiResponse(
                description='Successful response',
                response={
                    'type': 'object',
                    'properties': {
                        'risk_score': {'type': 'number'},
                        'risk_level': {'type': 'string'},
                        'risk_breakdown': {
                            'type': 'object',
                            'properties': {
                                'load_risk': {'type': 'number'},
                                'anomaly_risk': {'type': 'number'},
                                'forecast_risk': {'type': 'number'},
                            }
                        }
                    }
                },
                examples=[
                    OpenApiExample(
                        'Risk example',
                        value={
                            'risk_score': 0.61,
                            'risk_level': 'medium',
                            'risk_breakdown': {
                                'load_risk': 0.55,
                                'anomaly_risk': 0.70,
                                'forecast_risk': 0.40,
                            }
                        }
                    )
                ]
            ),
            204: OpenApiResponse(description='No data available'),
        }
    )
    def get(self, request):
        result = AnalysisResult.objects.order_by('-created_at').first()

        if not result or not (result.risk_score != None and result.risk_level and result.risk_breakdown):
            return Response({'message': 'no data available'}, status=204)

        return Response({
            'risk_score': result.risk_score,
            'risk_level': result.risk_level,
            'risk_breakdown': result.risk_breakdown
        })


class DecisionsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['analysis'],
        summary='Get Decisions',
        description='Returns the latest decisions from ML analysis.',
        responses={
            200: OpenApiResponse(
                description='Successful response',
                response={
                    'type': 'object',
                    'properties': {
                        'decisions': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'priority': {'type': 'integer'},
                                    'action': {'type': 'string'},
                                    'reason': {'type': 'string'},
                                    'urgency': {'type': 'string'},
                                }
                            }
                        }
                    }
                },
                examples=[
                    OpenApiExample(
                        'Decisions example',
                        value={
                            'decisions': [
                                {
                                    'priority': 1,
                                    'action': 'Check unit A status',
                                    'reason': 'Sudden increase in param1',
                                    'urgency': 'high',
                                }
                            ]
                        }
                    )
                ]
            ),
            204: OpenApiResponse(description='No data available'),
        }
    )
    def get(self, request):
        result = AnalysisResult.objects.order_by('-created_at').first()

        if not result or not result.decisions:
            return Response({'message': 'no data available'}, status=204)

        return Response({
            'decisions': result.decisions 
        })




from rest_framework.views import APIView
from rest_framework.response import Response
from core.cache import get_realtime_data
from .models import ProcessedData
from .serializers import TimeSeriesQuerySerializer
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse,
)
from drf_spectacular.types import OpenApiTypes
from rest_framework.permissions import IsAuthenticated


class RealtimeView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
            tags=['data'],
            summary='Get Real-Time Data',
            description='Returns the latest values from Redis, falls back to PostgreSQL if Redis is empty.',
            responses={
                200:
                    OpenApiResponse(
                        description='Successful Response',
                        response={
                            'type': 'object',
                            'properties': {
                                'param1': {'type': 'number'},
                                'param2': {'type': 'number'},
                                'param3': {'type': 'number'},
                                'param4': {'type': 'number'},
                                'param5': {'type': 'number'},
                            }
                        },
                        examples=[OpenApiExample(
                            'Real-time data example',
                            value={
                                'param1': 245.6,
                                'param2': 63.2,
                                'param3': 1845.3,
                                'param4': 42.1,
                                'param5': 49.98,
                            }
                        )
                        ]
                    ),
                204: OpenApiResponse(description='No data available')
            }
    )
    def get(self, request):
        data = get_realtime_data()

        if all(v is None for v in data.values()):
            last = ProcessedData.objects.order_by('-timestamp').first()
            if last:
                data = {
                    'param1': last.param1,
                    'param2': last.param2,
                    'param3': last.param3,
                    'param4': last.param4,
                    'param5': last.param5,
                }
            else:
                return Response({'message': 'no data available'}, status=204)

        return Response(data)


class TimeSeriesView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
            tags=['data'],
            summary='Get Time-series Data',
            description='Returns time-series data filtered by parameter and date range.',
            parameters=[
                OpenApiParameter(
                    name='param',
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.QUERY,
                    description='Parameter name (default: param1)',
                    required=False,
                    enum=['param1', 'param2', 'param3', 'param4', 'param5']
                ),
                OpenApiParameter(
                    name='from_time',
                    type=OpenApiTypes.DATETIME,
                    location=OpenApiParameter.QUERY,
                    description='Start time (ISO 8601 format)',
                    required=False,
                    examples=[OpenApiExample('example', value='2026-08-01T00:00:00Z')],
                ),
                OpenApiParameter(
                    name='to_time',
                    type=OpenApiTypes.DATETIME,
                    location=OpenApiParameter.QUERY,
                    description='End time (ISO 8601 format)',
                    required=False,
                    examples=[OpenApiExample('example', value='2026-08-16T23:59:59Z')],
                ),
            ],
            responses={
                200: OpenApiResponse(
                    description='Successful response',
                    response={
                        'type': 'object',
                        'properties': {
                            'param': {'type': 'string'},
                            'data': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'timestamp': {'type': 'string', 'format':'date-time'},
                                        'value': {'type': 'number',},
                                    }
                                }
                            }
                        }
                    },
                    examples=[OpenApiExample(
                        'Time-series example',
                        value={
                            'param': 'param1',
                            'data': [
                                {
                                    'timestamp': '2026-08-22T13:31:00Z',
                                    'value': 62.26
                                },
                                {
                                    'timestamp': '2026-08-22T13:30:00Z',
                                    'value': 58.14
                                },
                                {
                                    'timestamp': '2026-08-22T13:29:00Z',
                                    'value': 71.89
                                }
                            ]
                        }
                    )]
                ),
                204: OpenApiResponse(description='no data available'),
                400: OpenApiResponse(description='invalid parameters')
            }
    )
    def get(self, request):
        serializer = TimeSeriesQuerySerializer(data=request.query_params)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        validated_data = serializer.validated_data
        param = validated_data.get('param', 'param1')
        from_time = validated_data.get('from_time')
        to_time = validated_data.get('to_time')

        queryset = ProcessedData.objects.all()

        if from_time:
            queryset = queryset.filter(timestamp__gte=from_time)

        if to_time:
            queryset = queryset.filter(timestamp__lte=to_time)

        queryset = queryset.order_by('-timestamp')[:1000]

        data = []

        for obj in queryset:
            data.append({
                'timestamp': obj.timestamp,
                'value': getattr(obj, param)
            })

        if not data:
            return Response({'message': 'no data available'}, status=204)

        return Response({
            'param': param,
            'data': data
        })

        

        

                
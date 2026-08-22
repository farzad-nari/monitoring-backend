from rest_framework.views import APIView
from rest_framework.response import Response
from core.cache import get_realtime_data
from .models import ProcessedData
from .serializers import TimeSeriesQuerySerializer


class RealtimeView(APIView):
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

        

        

                
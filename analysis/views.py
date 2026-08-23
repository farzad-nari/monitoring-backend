from rest_framework.views import APIView
from rest_framework.response import Response
from .models import AnalysisResult


class ForecastView(APIView):
    def get(self, request):
        result = AnalysisResult.objects.order_by('-created_at').first()

        if not result or not result.forecast:
            return Response({'message': 'no data available'}, status=204)

        return Response({'forecast': result.forecast})


class AnomaliesView(APIView):
    def get(self, request):
        result = AnalysisResult.objects.order_by('-created_at').first()

        if not result or not result.anomalies:
            return Response({'message': 'no data available'}, status=204)

        return Response({'anomalies': result.anomalies})


class RiskView(APIView):
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
    def get(self, request):
        result = AnalysisResult.objects.order_by('-created_at').first()

        if not result or not result.decisions:
            return Response({'message': 'no data available'}, status=204)

        return Response({
            'decisions': result.decisions 
        })




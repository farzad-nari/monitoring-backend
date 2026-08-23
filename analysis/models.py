from django.db import models
from data.models import ProcessingJob


class AnalysisResult(models.Model):
    job = models.OneToOneField(ProcessingJob, on_delete=models.CASCADE, related_name='analysis_result')
    request_id = models.UUIDField()
    processed_at = models.DateTimeField()
    forecast = models.JSONField(null=True, blank=True)
    risk_score = models.FloatField(null=True, blank=True)
    risk_level = models.CharField(max_length=50, null=True, blank=True)
    risk_breakdown = models.JSONField(null=True, blank=True)
    anomalies = models.JSONField(null=True, blank=True)
    decisions = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'analysis_results'
        ordering = ['-created_at']

    def __str__(self):
        return f"AnalysisResult for Job {self.job_id}"
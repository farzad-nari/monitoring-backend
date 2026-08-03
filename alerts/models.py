from django.db import models
from data.models import ProcessingJob
from analysis.models import AnalysisResult
from django.conf import settings


class Alert(models.Model):
    SEVERITY_CHOICES = [
        ('warning', 'Warning'),
        ('critical', 'Critical'),
    ]

    job = models.ForeignKey(ProcessingJob, on_delete=models.CASCADE, related_name='alerts')
    analysis_result = models.ForeignKey(
        AnalysisResult,
        on_delete=models.CASCADE, 
        related_name='alerts', null=True,
        blank=True
    )
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    param = models.CharField(max_length=50)
    message = models.TextField()
    actual_value = models.FloatField(null=True, blank=True)
    threshold_value = models.FloatField(null=True, blank=True)
    unit_id = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_acknowledged = models.BooleanField(default=False)
    acknowledged_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'alerts'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.severity}: {self.message[:50]}'

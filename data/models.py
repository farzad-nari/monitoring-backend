from django.db import models
import uuid


class RawData(models.Model):
    timestamp = models.DateTimeField()
    param1 = models.FloatField()
    param2 = models.FloatField()
    param3 = models.FloatField()
    param4 = models.FloatField()
    param5 = models.FloatField()
    unit_id = models.CharField(max_length=50, blank=True, null=True)
    equipment_status = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'raw_data'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"RawData {self.timestamp}"


class ProcessingJob(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    request_id = models.UUIDField(default=uuid.uuid4, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    window_size = models.IntegerField(default=288)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:    
        db_table = 'processing_jobs'
        ordering = ['-created_at']

    def __str__(self):
        return f"Job {self.id} - {self.created_at}" 

    
class ProcessedData(models.Model):
    raw_data = models.OneToOneField(
        RawData,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='processed_data'
    )
    job = models.ForeignKey(ProcessingJob, on_delete=models.CASCADE, related_name='processed_data')

    timestamp = models.DateTimeField()
    param1 = models.FloatField()
    param2 = models.FloatField()
    param3 = models.FloatField()
    param4 = models.FloatField()
    param5 = models.FloatField()
    unit_id = models.CharField(max_length=50, blank=True, null=True)
    equipment_status = models.CharField(max_length=50, blank=True, null=True)

    param1_ma5m = models.FloatField(null=True, blank=True)
    param1_ma15m = models.FloatField(null=True, blank=True)
    param1_ma30m = models.FloatField(null=True, blank=True)
    param1_change_rate = models.FloatField(null=True, blank=True)
    param2_change_rate = models.FloatField(null=True, blank=True)
    hour_of_day = models.IntegerField(null=True, blank=True)
    day_of_week = models.IntegerField(null=True, blank=True)
    month = models.IntegerField(null=True, blank=True)
    param1_deviation_7d = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'processed_data'
        ordering = ['-timestamp']
        indexes = [
             models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"ProcessedData {self.timestamp}"
         


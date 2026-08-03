from django.contrib import admin
from .models import RawData, ProcessingJob, ProcessedData


admin.site.register(RawData)
admin.site.register(ProcessingJob)
admin.site.register(ProcessedData)

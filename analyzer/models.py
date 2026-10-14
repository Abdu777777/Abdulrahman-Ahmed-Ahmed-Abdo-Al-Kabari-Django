from django.conf import settings
from django.db import models
class RoundRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="round_records")
    session_name = models.CharField(max_length=120, blank=True, default="")
    row_number = models.PositiveSmallIntegerField(default=1)
    multiplier = models.CharField(max_length=32, blank=True, default="")
    predictions = models.JSONField(default=list)
    actuals = models.JSONField(default=list)
    notes = models.CharField(max_length=500, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created_at"]
    def as_dict(self):
        return {"id":self.id,"session_name":self.session_name,"row_number":self.row_number,"multiplier":self.multiplier,"predictions":self.predictions,"actuals":self.actuals,"notes":self.notes,"created_at":self.created_at.isoformat()}

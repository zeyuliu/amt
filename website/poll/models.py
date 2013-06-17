from django.db import models

from website.settings import PROJECT_ROOT

# Create your models here.
class Subject(models.Model):
    # The worker id assigned by AMT so we can identify participants
    worker_id = models.CharField(max_length=128)
    # The id assigned by AMT for this hit
    hit_id = models.CharField(max_length=128)
    # Whether the participant was debriefed
    debriefed = models.BooleanField(default=False)
    # The time the hit was started
    time_started = models.DateTimeField(db_index=True)
    # The time the hit was completed
    time_completed = models.DateTimeField(db_index=True, blank=True, null=True)
    # Whether the hit was abandoned
    abandoned = models.BooleanField(default=False)

    def __unicode__(self):
        return "Subject " + worker_id + " - " + str(image_group.pk)

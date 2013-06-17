from django.db import models
from poll.models import Subject

# Create your models here.

class ImageGroup(models.Model):
    # Status of the image group
    # 0 if unassigned and incomplete
    # 1 if assigned
    # 2 if completed
    status = models.IntegerField()
    subject = models.ForeignKey(Subject, blank=True, null=True)

    def __unicode__(self):
        image_set = 'Images'
        for image in self.image_set.all():
            image_set += ' ' + image.__unicode__()
        return image_set

class Image(models.Model):
    ranking = models.IntegerField(default=-1)
    image_group = models.ForeignKey(ImageGroup)
    image_id = models.CharField(max_length=30)

    def __unicode__(self):
        return str(self.image_id)

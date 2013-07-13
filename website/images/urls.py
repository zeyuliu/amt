from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url

from images.views import landing
from images.views import display
from images.views import debrief
from images.views import thankyou
from images import form_views

urlpatterns = patterns('',
    url(r'^landing/$', landing, name='amt-image-landing'),
    url(r'^$', landing, name='amt-image-home'),
    #url(r'^view-images/(?P<amt>\d)/(?P<assignmentId>\w+)/(?P<hitId>\w+)/$',
     #   display, name='amt-image-poll'),
    url(r'^view-images/$', display, name='amt-image-poll'),
    url(r'^submit-image-scores/$', form_views.MTurkImages.as_view(), name='image-score-submission'),
    url(r'^debrief/$', debrief, name='amt-image-poll-debrief'),
    url(r'^thanks/$', thankyou, name='amt-image-poll-thanks'),
)

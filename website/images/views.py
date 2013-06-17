from datetime import datetime

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import Http404
from django.template import RequestContext

from images.models import Image
from images.models import ImageGroup
from images.utils import assign_image_group
from poll.models import Subject

# Create your views here

def landing(request, template_name='amt/images/landing.html'):
    """
    Landing view for external url. This page provides a consent form.
    Only after acceptance of the consent form can the user participate in the study.
    """
    # Data to render to template
    data = {'amt': int(False)}
    # We want to allow regular people to perform this hit as well
    # If the request does not contain amt context, we should
    # still let them perform the experiment
    assignmentId = request.GET.get('assignmentId', default=None)
    hitId = request.GET.get('hitId', default=None)
    if assignmentId and hitId:
        # Create a Subject object
	subject = Subject(
	worker_id=assignmentId,
	hit_id=hitId,
	debriefed=False,
	time_started=datetime.utcnow(),
	time_completed=None
	)
	subject.save()
        data['amt'] = int(True)
    data['assignmentId'] = assignmentId
    data['hitId'] = hitId
        
    return render_to_response(template_name, data, context_instance=RequestContext(request))

def display(request, template_name='amt/images/main.html'):
    if request.GET.get('amt', None) == 1:
	assignmentId = request.GET.get('assignmentId', default=None)
	hitId = request.GET.get('hitId', default=None)
	if assignmentId and hitId:
	    # Find the subject
	    try:
		subject = Subject.objects.get(
		    worker_id=assignmentId,
		    hit_id=hitId,
		    time_completed__isnull=True
		)
	    except Subject.DoesNotExist:
		return HttpReponse("hi")
        
        image_group = assign_image_group(subject)
    else:
        image_group = assign_image_group()
    return render_to_response(template_name, {'images':image_group.image_set.all()}, context_instance=RequestContext(request))

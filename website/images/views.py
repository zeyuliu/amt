import urllib2
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
    # Will not have worker id until AFTER they have accepted the HIT
    workerId = request.GET.get('workerId', default=None)
    if assignmentId and hitId and workerId:
        data['amt'] = int(True)
    data['assignmentId'] = assignmentId
    data['hitId'] = hitId
    return render_to_response(template_name, data, context_instance=RequestContext(request))

def display(request, template_name='amt/images/main.html'):
    amt = request.GET.get('amt', None)
    assignmentId = request.GET.get('assignmentId', default=None)
    hitId = request.GET.get('hitId', default=None)
    if amt == 1 and assignmentId and hitId:
    # Create a Subject object
        subject = Subject(
            worker_id=assignmentId,
            hit_id=hitId,
            debriefed=False,
            time_started=datetime.utcnow(),
            time_completed=None
        )
        subject.save()
        # Check if an image group already exists for the subject:
        image_group = ImageGroup.objects.filter(subject=subject)
        if image_group:
            image_group = image_group[0]
        else:
            image_group = assign_image_group(subject)
    else:
        image_group = assign_image_group()
    data = {
        'assignmentId': assignmentId,
        'hitId': hitId,
        'amt': amt,
        'images': image_group.image_set.all()
    }
    return render_to_response(template_name, data, context_instance=RequestContext(request))

def debrief(request, template_name='amt/images/debrief.html'):
    amt = request.GET.get('amt', None)
    assignmentId = request.GET.get('assignmentId', default=None)
    hitId = request.GET.get('hitId', default=None)
    if amt == 1 and assignmentId and hitId:
        try:
            # Grab subject
            subject = Subject.objects.filter(
                worker_id=assignmentId,
                hit_id=hitId,
                debriefed=False,
                time_completed__isnull=True
            ).latest('time_started')
            subject.debriefed=True
            subject.time_completed=datetime.utcnow()
            subject.save()
        except Subject.DoesNotExist:
            return HttpResponse('Sorry, an error has occurred. Please make sure you did not press the back button.', status=400)

    data = {
        'assignmentId': assignmentId,
        'hitId': hitId,
        'amt': amt,
    }
    return render_to_response(template_name, data, context_instance=RequestContext(request))

def thankyou(request, template_name='amt/images/thankyou.html'):
    amt = request.GET.get('amt', None)
    assignmentId = request.GET.get('assignmentId', default=None)
    hitId = request.GET.get('hitId', default=None)
    decision = request.GET.get('decision', default=None)
    if amt == 1:
        # pay the participant
        url = 'https://workersandbox.mturk.com/mturk/externalSubmit'
        post_data = {
                'assignmentId' : assignmentId,
                'hitId': hitId,
                'workerId'
        if assignmentId and hitId and decision == 0:
            try:
                # Grab subject
                subject = Subject.objects.filter(
                    worker_id=assignmentId,
                    hit_id=hitId,
                    debriefed=True,
                    time_completed__isnull=True
                ).latest('time_started')
                # Grab the Image Group for the subject
                image_group = ImageGroup.objects.filter(subject=subject)
                if image_group:
                    image_group = image_group[0]
                    image_group.image_set.update(deleted=True)
            except Subject.DoesNotExist:
                return HttpResponse('Sorry, an error has occurred. Please make sure you did not press the back button.', status=400)
    return render_to_response(template_name, context_instance=RequestContext(request))

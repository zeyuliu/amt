from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseForbidden
from django.utils import simplejson
from django.views.decorators.http import require_POST
from django.views.generic import FormView

from images.models import Image
from images.models import ImageGroup
from images.forms import ImageGroupForm

class MTurkImages(FormView):
    form_class = ImageGroupForm

    def post(self, request):
        form = self.form_class(request.POST)
        # Checks to make sure that the form has valid input
        if not form.is_valid():
            return HttpResponseBadRequest(
               simplejson.dumps({'errors': form.errors}),
               content_type='application/json'
            )
        form.clean()
        # Find the ImageGroup

        image_group = ImageGroup.objects.get(pk = form.data['image_group_id'], status=1)
        image_group.status = 2
        image_group.save()

        # Creates Image objects
        image1 = image_group.image_set.get(
                    image_id=form.data['p1_id']
                    )
        image1.ranking = form.data['p1_score']
        image1.save()

        image2 = image_group.image_set.get(
                    image_id=form.data['p2_id']
                    )
        image2.ranking = form.data['p2_score']
        image2.save()

        image3 = image_group.image_set.get(
                    image_id=form.data['p3_id']
                    )
        image3.ranking = form.data['p3_score']
        image3.save()

        image4 = image_group.image_set.get(
                    image_id=form.data['p4_id']
                    )
        image4.ranking = form.data['p4_score']
        image4.save()

        image5 = image_group.image_set.get(
                    image_id=form.data['p5_id']
                    )
        image5.ranking = form.data['p5_score']
        image5.save()

        image6 = image_group.image_set.get(
                    image_id=form.data['p6_id']
                    )
        image6.ranking = form.data['p6_score']
        image6.save()
        msg = 'Image scores have been saved'
        # ADD some kind of redeem code that allows users to redeem reward on AMT
        return HttpResponse(
            simplejson.dumps(
                {'success': 'true',
                'msg': msg
                }
            ),
            content_type='application/json'
        )

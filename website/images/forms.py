from django import forms
from django.db import models
from images.models import ImageGroup


class ImageGroupForm(forms.Form):
    # Score given for each picture
    p1_score = models.IntegerField()
    p2_score = models.IntegerField()
    p3_score = models.IntegerField()
    p4_score = models.IntegerField()
    p5_score = models.IntegerField()
    p6_score = models.IntegerField()

    # Picture ID
    p1_id = models.CharField()
    p2_id = models.CharField()
    p3_id = models.CharField()
    p4_id = models.CharField()
    p5_id = models.CharField()
    p6_id = models.CharField()

    # ImageGroup ID
    # This is actually the pk for the ImageGroup in our db
    image_group_id = models.IntegerField()


    # Maybe we should clean image ids at some point too?

    def clean_image_group_id(self):
        try:
            # Find ImageGroup
            image_group = ImageGroup.objects.get(pk=image_group_id,status=1)
            # Find images
            image1 = Image.objects.get(image_id=p1_id)
            image2 = Image.objects.get(image_id=p2_id)
            image3 = Image.objects.get(image_id=p3_id)
            image4 = Image.objects.get(image_id=p4_id)
            image5 = Image.objects.get(image_id=p5_id)
            image6 = Image.objects.get(image_id=p6_id)
            # Make sure that images are in the ImageGroup's image_set
            image_set = image_group.image_set.all()
            if not (image1 in image_set and
                    image2 in image_set and
                    image3 in image_set and
                    image4 in image_set and
                    image5 in image_set and
                    image6 in image_set):
                raise forms.ValidationError("Invalid set of images.")
            return image_group.id
        except:
            raise forms.ValidationError("Invalid set of images.")



        

    def clean_p1_score(self):
        # Default score max value is 6
        # Default score min value is 1
        if self.cleaned_data['p1_score'] > 6 or self.cleaned_data['p1_score'] < 1:
            raise forms.ValidationError("Score for picture 1 is not valid.")
        return self.cleaned_data['p1_score']


    def clean_p2_score(self):
        # Default score max value is 6
        # Default score min value is 1
        if self.cleaned_data['p2_score'] > 6 or self.cleaned_data['p2_score'] < 1:
            raise forms.ValidationError("Score for picture 2 is not valid.")
        return self.cleaned_data['p2_score']

    def clean_p3_score(self):
        # Default score max value is 6
        # Default score min value is 1
        if self.cleaned_data['p3_score'] > 6 or self.cleaned_data['p3_score'] < 1:
            raise forms.ValidationError("Score for picture 3 is not valid.")
        return self.cleaned_data['p3_score']

    def clean_p4_score(self):
        # Default score max value is 6
        # Default score min value is 1
        if self.cleaned_data['p4_score'] > 6 or self.cleaned_data['p4_score'] < 1:
            raise forms.ValidationError("Score for picture 4 is not valid.")
        return self.cleaned_data['p4_score']

    def clean_p5_score(self):
        # Default score max value is 6
        # Default score min value is 1
        if self.cleaned_data['p5_score'] > 6 or self.cleaned_data['p5_score'] < 1:
            raise forms.ValidationError("Score for picture 5 is not valid.")
        return self.cleaned_data['p5_score']

    def clean_p6_score(self):
        # Default score max value is 6
        # Default score min value is 1
        if self.cleaned_data['p6_score'] > 6 or self.cleaned_data['p6_score'] < 1:
            raise forms.ValidationError("Score for picture 6 is not valid.")
        return self.cleaned_data['p6_score']

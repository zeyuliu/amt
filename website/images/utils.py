import csv

from website.settings import PROJECT_ROOT
from images.models import Image
from images.models import ImageGroup

def bulk_add_images(path):
    try:
        import pdb; pdb.set_trace()
        csv_file = open(PROJECT_ROOT + "/" + path)
        file_reader = csv.reader(csv_file, delimiter=',', quotechar='|')
        reader_as_list = list(file_reader)
        for group in reader_as_list:
            image_group = ImageGroup(status=0)
            image_group.save()
            for image_id in group:
                image = Image(image_id=image_id, image_group=image_group)
                image.save()
        csv_file.close()
    except Error as e:
        print("Corrupt file format")

def assign_image_group(subject=None):
    # Automatically assigns the next unassigned and incomplete image group
    image_groups = ImageGroup.objects.filter(status=0)
	# Testing
    if len(image_groups) == 0:
        ImageGroup.objects.all().update(status=0)
        image_groups = ImageGroup.objects.all()
    image_group = image_groups[0]
    image_group.status=1
    image_group.save()
    return image_group

from django.conf import settings

from . import models

def trending(request):
    return {"trends" : models.Question.objects.all().order_by('-rating')[:settings.TRENDS_PER_PAGE],}

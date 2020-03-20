from django.views.decorators.http import require_safe
from django.shortcuts import redirect, render, reverse

@require_safe
def home_view(request):
    # return render(request, 'base.html')
    return redirect(reverse('qanda:questions_list'))


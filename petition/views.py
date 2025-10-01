from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Petition
import json


def index(request):
    # Show all petitions newest first
    petitions = Petition.objects.all().order_by('-date')
    template_data = {
        'title': 'Petition',
        'petitions': petitions,
    }
    return render(request, 'petition/index.html', {'template_data': template_data})


@login_required
def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if not title or not title.strip():
            template_data = {
                'title': 'Petition',
                'error': 'Please enter a movie title.',
                'petitions': Petition.objects.all().order_by('-date')
            }
            return render(request, 'petition/index.html', {'template_data': template_data})
        Petition.objects.create(title=title.strip(), user=request.user)
        return redirect('petition.index')
    return HttpResponseBadRequest('Invalid method')


@login_required
def toggle_like(request, id):
    # Expect AJAX POST with JSON body
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid method')

    petition = get_object_or_404(Petition, id=id)

    # Toggle like
    if request.user in petition.likes.all():
        petition.likes.remove(request.user)
        liked = False
    else:
        petition.likes.add(request.user)
        liked = True

    return JsonResponse({'liked': liked, 'likes_count': petition.likes.count()})

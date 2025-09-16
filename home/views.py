from django.shortcuts import render
from movies.models import Review
from django.core.paginator import Paginator
def index(request):
    template_data = {}
    template_data['title'] = 'Movies Store'
    return render(request, 'home/index.html', {'template_data': template_data})
def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request, 'home/about.html', {'template_data': template_data})

def reviews(request):
    """Show all reviews across all movies, newest first, paginated."""
    # Order primarily by rating (highest first), then by date (newest first)
    reviews_qs = Review.objects.select_related('movie', 'user').order_by('-rating', '-date')
    paginator = Paginator(reviews_qs, 10)  # 10 reviews per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template_data = {}
    template_data['title'] = 'All Reviews'
    template_data['page_obj'] = page_obj
    return render(request, 'home/reviews.html', {'template_data': template_data})

# Create your views here.

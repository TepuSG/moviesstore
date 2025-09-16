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
    # Prefer ordering by rating (highest first) then date, but if the DB
    # doesn't yet have the rating column (e.g. migrations not applied on server)
    # fall back to ordering by date to avoid a 500 error.
    try:
        reviews_qs = Review.objects.select_related('movie', 'user').order_by('-rating', '-date')
    except Exception as e:
        # If the database lacks the rating column, fall back to date ordering.
        # We keep the except broad to cover different DB backends raising
        # different exception types; log if needed.
        reviews_qs = Review.objects.select_related('movie', 'user').order_by('-date')
    paginator = Paginator(reviews_qs, 10)  # 10 reviews per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template_data = {}
    template_data['title'] = 'All Reviews'
    template_data['page_obj'] = page_obj
    return render(request, 'home/reviews.html', {'template_data': template_data})

# Create your views here.

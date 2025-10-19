from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, Rating
from .forms import RatingForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_POST
def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else: 
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html', {'template_data': template_data})
def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    
    # Rating-related data
    user_rating = None
    if request.user.is_authenticated:
        try:
            user_rating = Rating.objects.get(user=request.user, movie=movie)
        except Rating.DoesNotExist:
            pass
    
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    template_data['user_rating'] = user_rating
    template_data['average_rating'] = movie.average_rating()
    template_data['rating_count'] = movie.rating_count()
    template_data['rating_form'] = RatingForm()
    
    return render(request, 'movies/show.html', {'template_data': template_data})
@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment']!= '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        # Accept rating if provided, otherwise default in model
        try:
            review.rating = int(request.POST.get('rating', review.rating))
        except Exception:
            pass
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)


@login_required
def toggle_like(request, id, review_id):
    # Toggle a like on a review. Accepts POST only.
    if request.method != 'POST':
        return HttpResponseForbidden()
    review = get_object_or_404(Review, id=review_id)
    if request.user in review.likes.all():
        review.likes.remove(request.user)
        liked = False
    else:
        review.likes.add(request.user)
        liked = True
    # If this was ajax, return json with updated count
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'likes_count': review.likes.count()})
    return redirect('movies.show', id=id)
@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html',
            {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id,
        user=request.user)
    review.delete()
    return redirect('movies.show', id=id)


@login_required
@require_POST
def submit_rating(request, id):
    """Handle rating submission via AJAX"""
    movie = get_object_or_404(Movie, id=id)
    
    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'error': 'AJAX required'}, status=400)
    
    try:
        rating_value = int(request.POST.get('rating'))
        if rating_value < 1 or rating_value > 5:
            return JsonResponse({'error': 'Rating must be between 1 and 5'}, status=400)
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid rating value'}, status=400)
    
    # Create or update the rating
    rating, created = Rating.objects.update_or_create(
        user=request.user,
        movie=movie,
        defaults={'rating': rating_value}
    )
    
    # Return updated data
    return JsonResponse({
        'success': True,
        'user_rating': rating.rating,
        'average_rating': round(movie.average_rating(), 1),
        'rating_count': movie.rating_count(),
        'created': created
    })


# Create your views here.

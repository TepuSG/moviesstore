from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from movies.models import Movie
from cart.models import Order, Item
from django.contrib.auth.decorators import login_required 
from django.http import JsonResponse
from django.db.models import Count
from .utils import calculate_cart_total


def index(request):
    cart_total = 0
    movies_in_cart = []
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if (movie_ids != []):
        movies_in_cart = Movie.objects.filter(id__in=movie_ids)
        cart_total = calculate_cart_total(cart,
            movies_in_cart)
    template_data = {}
    template_data['title'] = 'Cart'
    template_data['movies_in_cart'] = movies_in_cart
    template_data['cart_total'] = cart_total
    return render(request, 'cart/index.html',
        {'template_data': template_data})
def add(request, id):
    get_object_or_404(Movie, id=id)
    cart = request.session.get('cart', {})
    cart[id] = request.POST['quantity']
    request.session['cart'] = cart
    return redirect('cart.index')
def clear(request):
    request.session['cart'] = {}
    return redirect('cart.index')


@login_required
def purchase(request):
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if (movie_ids == []):
        return redirect('cart.index')
    movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    cart_total = calculate_cart_total(cart, movies_in_cart)


    if request.method == 'POST':
        location = request.POST.get('location', '').strip()
        order = Order.objects.create(user=request.user, total=cart_total, location=location)
        for movie in movies_in_cart:
            Item.objects.create(
                movie=movie,
                price=movie.price,
                order=order,
                quantity=cart[str(movie.id)]
            )
        request.session['cart'] = {}
        return render(request, 'cart/purchase.html', {'template_data': {'title': 'Purchase confirmation', 'order_id': order.id}})
    
    # Render form for location input
    return render(request, 'cart/confirm_location.html', {
        'movies_in_cart': movies_in_cart,
        'cart_total': cart_total
    })
# Create your views here


def trending_movies_api(request):
    data = (
        Item.objects
        .values('order__location', 'movie__name')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    result = {}
    for entry in data:
        loc = entry['order__location']
        if not loc:
            continue
        if loc not in result:
            result[loc] = []
        result[loc].append({'title': entry['movie__name'], 'count': entry['count']})
    return JsonResponse(result)
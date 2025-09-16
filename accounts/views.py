from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')
def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html',
                {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')
def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html',
                {'template_data': template_data})
@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html',
        {'template_data': template_data})


@login_required
def subscription(request):
    """Show the user's subscription level based on total lifetime spending.

    Rules:
      - Basic: total < 15
      - Medium: 15 <= total <= 30
      - Premium: total > 30
    """
    # Sum up all Order.total values for this user
    orders = request.user.order_set.all()
    total_spent = sum([o.total for o in orders]) if orders.exists() else 0

    # Determine level (totals are stored as integers matching Movie.price units)
    if total_spent < 15:
        level = 'Basic'
    elif total_spent <= 30:
        level = 'Medium'
    else:
        level = 'Premium'

    template_data = {
        'title': 'Subscription',
        'total_spent': total_spent,
        'level': level,
    }
    return render(request, 'accounts/subscription.html', {'template_data': template_data})
# Create your views here.

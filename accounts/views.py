from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contacts

# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            try:
                auth.login(request, user)
                messages.success(request, 'You are successfully loged in!')
                return redirect('dashboard')
            except Exception as error:
                messages.error(request, error)
        else:
            messages.error(request, 'Invalid credentials!')
            return redirect('login')

    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are successfully logged out!')
        return redirect('home')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        try:
            if len(password) >= 8:
                if password == password2:
                    if User.objects.filter(username=username).exists():
                        messages.error(request, 'Username Is Taken!')
                        return redirect('register')
                    else:
                        if User.objects.filter(email=email).exists():
                            messages.error(request, 'Username Is Taken!')
                            return redirect('register')
                        else:
                            try:
                                user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
                                user.save()
                                messages.success(request, 'You have successfully registered!')
                                return redirect('login')
                            except  Exception as error:
                                messages.error(request, error)
                                return redirect('register')
            else:
                messages.error(request, 'Password must be 8 characters or longer!')
                return redirect('register')

        except Exception as error:
            messages.error(request, error)
            return redirect('register')



        else:
            messages.error(request, 'Passwords Dont\'t Match!')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


def dashboard(request):
    user_contacts = Contacts.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context = {
        'contacts': user_contacts,
    }
    return render(request, 'accounts/dashboard.html', context)
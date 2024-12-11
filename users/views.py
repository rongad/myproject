from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Account successfully registered.")
                return redirect('homepage')
            except IntegrityError:
                messages.error(request, "Registration failed. Account already exists.")
        else:
            messages.error(request, "There was an error in the form.")
            print(form.errors)  # Print form errors for debugging
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            print(f"Attempting to authenticate user: {username}")  # Debug print
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print(f"User {username} logged in successfully")  # Debug print
                messages.success(request, "Login successful!")
                return redirect('homepage')
            else:
                print(f"Authentication failed for user: {username}")  # Debug print
                messages.error(request, "Account does not exist or invalid credentials.")
        else:
            print("Login form is invalid")  # Debug print
            print(form.errors)  # Print form errors for debugging
            messages.error(request, "Invalid login form.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('homepage')

@login_required
def homepage_view(request):
    return render(request, 'homepage.html')

from django.shortcuts import render, get_object_or_404, redirect
from .models import Transaction

@login_required
def add_transaction(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        amount = request.POST['amount']
        Transaction.objects.create(title=title, description=description, amount=amount)
        return redirect('homepage')
    return render(request, 'add_transaction.html')

@login_required
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        transaction.title = request.POST['title']
        transaction.description = request.POST['description']
        transaction.amount = request.POST['amount']
        transaction.save()
        return redirect('homepage')
    return render(request, 'edit_transaction.html', {'transaction': transaction})

@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        transaction.delete()
        return redirect('homepage')
    return render(request, 'delete_transaction.html', {'transaction': transaction})

@login_required
def view_transaction(request):
    transactions = Transaction.objects.all()
    return render(request, 'view_transaction.html', {'transactions': transactions})

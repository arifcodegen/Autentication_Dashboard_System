from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import CustomUserSerializer

# Registration view
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already exists'})

        # Create new user
        user = CustomUser.objects.create_user(username=username, email=email, password=password)

        # Log the user in
        login(request, user)

        return redirect('login')  # Redirect to home after successful login

    return render(request, 'register.html')


# Login view
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to home after successful login
        else:
            return render(request, 'login.html', {'error': 'Invalid email or password'})

    return render(request, 'login.html')


@login_required  # This decorator ensures that only logged-in users can access the dashboard
def dashboard_view(request):
    return render(request, 'dashboard.html')


def logout_view(request):
    logout(request)  # This logs out the user
    return redirect('login')


class UserDataView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this

    def get(self, request):
        # Serialize the data of the authenticated user
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)

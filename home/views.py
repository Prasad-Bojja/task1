from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from .models import CustomUser

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import CustomUser
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        user_type = request.POST.get('user_type')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address_line1 = request.POST.get('address_line1')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        profile_picture = request.FILES.get('profile_picture') 
        
    
        if password1 != password2:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})
        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'This User Already Exists'})
      
        user = CustomUser.objects.create_user(username=username, email=email)
        user.user_type = user_type
        user.first_name = first_name
        user.last_name = last_name
        user.address_line1 = address_line1
        user.city = city
        user.state = state
        user.pincode = pincode
        user.set_password(password1)
       
        if profile_picture:
            user.profile_picture = profile_picture
        
        user.save() 
        return redirect('login')
    else:
        return render(request, 'signup.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not CustomUser.objects.filter(username=username).exists():
            return render(request, 'login.html', {'error': 'Invalid username or password'})

       
        user = authenticate(username=username, password=password)


        if user is None:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
           
        else:
            login(request,user)
            return redirect('dashboard')
        

  
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    user = request.user
    return render(request, 'dashboard.html', {'user': user})


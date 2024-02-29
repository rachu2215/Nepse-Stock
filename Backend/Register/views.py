from django.shortcuts import render, redirect
from django.views import View
# Create your views here.
from .forms import UserCreationForm, UserLoginForm
from django.contrib.auth import authenticate, login,logout


class RegisterUserView(View):
    def get(self, request):
        form =UserCreationForm()
        context = {'form': form}
        return render(request, 'Register/register.html', context)
    
    def post(self, request):
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            print ('User created')
            print (form.cleaned_data)
        
        context= {'form': form}
        return render(request, 'Register/register.html', context)
class LoginUserView(View):
    def get(self, request):
        form = UserLoginForm()
        context = {'form': form}
        return render(request, 'Register/login.html', context)
    
    def post(self, request):
        form = UserLoginForm(request.POST)
        
        if form.is_valid():
            email= form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                
                return redirect('index')
            else:
              
                form.add_error(None, "Invalid username or password")
        
        context= {'form': form}
        return render(request, 'Register/login.html', context)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
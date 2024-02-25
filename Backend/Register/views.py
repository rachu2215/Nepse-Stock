from django.shortcuts import render
from django.views import View
# Create your views here.
from .forms import UserCreationForm, UserLoginForm

def index(request):
    return render(request, 'Register/index.html')

def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print ('User created')
            print (form.cleaned_data)
    context = {'form': form}
    return render(request, 'Register/register.html', context)

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
        form = UserLoginForm
        context = {'form': form}
        return render(request, 'Register/login.html', context)
    
    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            form.save()
        
        context= {'form': form}
        return render(request, 'Register/login.html', context)
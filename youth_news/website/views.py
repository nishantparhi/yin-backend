from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login
from .models import Contact

def index(request):
    return render(request, 'website/index.html')
    

def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')

    form = CreateUserForm()
    context = {'form': form}
    return render(request, 'registration/signup.html', context)

def single(request):
    return render(request, 'website/single.html')

def contactPage(request):
    if request.method =='POST':

        name = request.POST['txtName']
        email = request.POST['txtEmail']
        phone = request.POST['txtPhone']
        subject = request.POST['txtSubject']
        message = request.POST['txtMsg']

    #form_class = ContactForm
        contact = Contact (name = name , email= email, phone=phone, subject= subject, message= message)
        contact.save()
    return render(request, 'website/page-contact.html')

def dashboardPage(request):
    return render(request, 'website/dashboard.html')
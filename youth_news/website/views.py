from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUserForm, PostForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Contact, BlogPost
from .decorators import unauthentiated_user

def index(request):
    return render(request, 'website/index.html')
    
@unauthentiated_user
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

@login_required
def dashboardPage(request):
    return render(request, 'website/dashboard.html')



# View individual blog
def blog(request, slug):
    try:
        blogpost = BlogPost.objects.get(slug=slug)
        user = blogpost.user
    except:
        return render(request, 'website/page-404.html')
    
    # if blog is not active then don't show anyone
    if blogpost.status != 'ACTIVE':
        return render(request, 'website/page-404.html')

    context = {
        'blogpost':blogpost,
        'pub_user':user,
    }
    return render(request, 'website/single.html', context)

# Create a new post
@login_required
def createPost(request):
    user = request.user
    # print(request.POST)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            # form.save()
            post_item = form.save(commit=False)
            post_item.user = request.user
            # status
            blogStatus = request.POST.get('status', None)
            # print(request.POST, blogStatus)
            if ( blogStatus!=None) and (blogStatus == 'ACTIVE'):
                post_item.status = 'ACTIVE'
            else:
                post_item.status = 'PENDING'
            post_item.save()
            if post_item.status == 'ACTIVE':
                return redirect(f'/news/{post_item.slug}')
            else:
                return redirect('dashboard')
    else:
        form = PostForm()

        # if the user is core member or not
        isCore = False
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'core_content_writter':
            isCore = True

    return render(request, 'website/create_post.html', {'form':form, 'isCore': isCore})

# Edit a post
@login_required
def editPost(request, slug=None):
    item = get_object_or_404(BlogPost, slug=slug)
    # check for auth
    if item.user != request.user:
        return render(request, 'website/page-404.html')

    form = PostForm(request.POST or None ,instance=item)
    if form.is_valid():
        # form.save()
        post_item = form.save(commit=False)
        post_item.user = request.user
        # status
        blogStatus = request.POST.get('status', None)
        # print(request.POST, blogStatus)
        if ( blogStatus!=None) and (blogStatus == 'ACTIVE'):
            post_item.status = 'ACTIVE'
        else:
            post_item.status = 'PENDING'
        post_item.save()
        if post_item.status == 'ACTIVE':
            return redirect(f'/news/{post_item.slug}')
        else:
            return redirect('dashboard')
    
    # if the user is core member or not
    isCore = False
    group = None
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name
    if group == 'core_content_writter':
        isCore = True
    return render(request, 'website/create_post.html', {'form':form, 'isCore': isCore})

# View Blogs
@login_required
def viewBlogs(request):
    return render(request, 'website/view_blogs.html')

# Pending Blogs
@login_required
def pendingBlogs(request):
    return render(request, 'website/pending_blogs.html')
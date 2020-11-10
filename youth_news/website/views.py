from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUserForm, PostForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Contact, BlogPost, Catagory, Author, Comment, Tag
from .decorators import unauthentiated_user, notDeveloper, onlyDeveloper
from django.contrib.auth.models import User


def index(request):
    trandingBlogs = BlogPost.objects.filter(
        isTranding=True).order_by('-pub_date')[:5]
    trandingCatagories = Catagory.objects.filter(
        tranding=True).order_by('-date')[:6]

    trandingCatagoriesPosts = []

    for i in trandingCatagories:
        trandingCatagoriesPosts.append(
            [i, BlogPost.objects.filter(catagory=i).filter(status="ACTIVE").order_by('-pub_date')])

    recentPosts = BlogPost.objects.all().order_by('-pub_date')[:3]
    popularPosts = BlogPost.objects.all().order_by('-views')[:3]
    popularCatagories = Catagory.objects.filter(
        tranding=True).order_by('-date')
    popularCatagoriesDict = {}
    for i in popularCatagories:
        popularCatagoriesDict[i] = len(BlogPost.objects.filter(catagory=i))
    # print(trandingCatagoriesPosts)
    context = {'trandingPosts': trandingBlogs,
               'trendingPostContent':  trandingCatagoriesPosts,
               'recentPosts': recentPosts,
               'popularPosts': popularPosts,
               'popularCatagoriesDict': popularCatagoriesDict}
    return render(request, 'website/index.html', context)


# def single(request, id):
#     blogs = BlogPost.objects.get(id=id)
#     # print(blogs)
#     context = {
#         'blogs': blogs,
#     }
#     return render(request, 'website/single.html', context)


def blogauthor(request, username):
    user = User.objects.get(username=username)
    # print(user)
    blogs = BlogPost.objects.filter(user=user)
    author = Author.objects.get(user=user)
    # print(blogs)
    recentPosts = BlogPost.objects.all().order_by('-pub_date')[:3]
    popularPosts = BlogPost.objects.all().order_by('-views')[:3]
    popularCatagories = Catagory.objects.filter(
        tranding=True).order_by('-date')
    popularCatagoriesDict = {}
    for i in popularCatagories:
        popularCatagoriesDict[i] = len(BlogPost.objects.filter(catagory=i))
    context = {
        'blogs': blogs,
        'author': author,
        'recentPosts': recentPosts,
        'popularPosts': popularPosts,
        'popularCatagoriesDict': popularCatagoriesDict
    }
    return render(request, 'website/blog-author.html', context)


def trendingCategories_processor(request):
    trandingCatagories = Catagory.objects.filter(
        tranding=True).order_by('-date')[:6]
    # print(BlogPost.objects.filter(catagory=trandingCatagories[1]))
    # print(trandingCatagories[0])
    trandingCatagoriesPosts = []
    # for i in range(len(trandingCatagories)):
    #     trandingCatagoriesPosts.append(
    #         BlogPost.objects.filter(catagory=trandingCatagories[i]))

    for i in trandingCatagories:
        trandingCatagoriesPosts.append(
            BlogPost.objects.filter(catagory=i).filter(status="ACTIVE"))
    # print(trandingCatagoriesPosts[0][0].getFirstTag)
    return {'trandingCatagories': trandingCatagories, 'trandingCatagoriesPosts': zip(trandingCatagories, trandingCatagoriesPosts)}


@ unauthentiated_user
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
    if request.method == 'POST':

        name = request.POST['txtName']
        email = request.POST['txtEmail']
        phone = request.POST['txtPhone']
        subject = request.POST['txtSubject']
        message = request.POST['txtMsg']

    # form_class = ContactForm
        contact = Contact(name=name, email=email, phone=phone,
                          subject=subject, message=message)
        contact.save()
    recentPosts = BlogPost.objects.all().order_by('-pub_date')[:3]
    popularPosts = BlogPost.objects.all().order_by('-views')[:3]
    popularCatagories = Catagory.objects.filter(
        tranding=True).order_by('-date')
    popularCatagoriesDict = {}
    for i in popularCatagories:
        popularCatagoriesDict[i] = len(BlogPost.objects.filter(catagory=i))
    context = {'recentPosts': recentPosts, 'popularPosts': popularPosts,
               'popularCatagoriesDict': popularCatagoriesDict}
    return render(request, 'website/page-contact.html', context)


@ login_required
@ notDeveloper()
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

    # add view count
    blogpost.views = blogpost.views + 1
    blogpost.save()
    recentPosts = BlogPost.objects.all().order_by('-pub_date')[:3]
    popularPosts = BlogPost.objects.all().order_by('-views')[:3]
    popularCatagories = Catagory.objects.filter(
        tranding=True).order_by('-date')
    popularCatagoriesDict = {}
    for i in popularCatagories:
        popularCatagoriesDict[i] = len(BlogPost.objects.filter(catagory=i))
    author = Author.objects.get(user=user)
    realatedPost = BlogPost.objects.filter(
        catagory=blogpost.catagory.first()).filter(status="ACTIVE").order_by('-pub_date')[:2]
    prevNextPost = BlogPost.objects.filter(
        user=blogpost.user).filter(status="ACTIVE").exclude(id=blogpost.id).order_by('-pub_date')[:2]
    print(prevNextPost[0].coverPic)
    comments = Comment.objects.filter(blog=blogpost)
    context = {
        'blogpost': blogpost,
        'author': author,
        'recentPosts': recentPosts,
        'popularPosts': popularPosts,
        'realatedPost': realatedPost,
        'prevNextPost': prevNextPost,
        'comments': comments,
        'popularCatagoriesDict': popularCatagoriesDict
    }
    return render(request, 'website/single.html', context)


# Create a new post
@login_required
@notDeveloper()
def createPost(request):
    user = request.user
    if request.method == "POST":
        print(request.FILES)
        print(request.FILES)
        print(request.FILES)
        blogpost = BlogPost.objects.create(
            user=request.user,
            blog_title=request.POST.get('blog_title'),
            blog_content=request.POST.get('blog_content'),
            status=request.POST.get('status'),
            coverPic=request.FILES.get('myfile')


        )
        for id in request.POST.get('selectedCat').split(','):
            try:
                test = int(id)
                blogpost.catagory.add(id)
            except:
                pass
        for id in request.POST.get('selectedTag').split(','):
            try:
                test = int(id)
                blogpost.tags.add(id)
            except:
                pass
        blogpost.save()

    allCategories = Catagory.objects.all()
    allTags = Tag.objects.all()
    form = PostForm()
    isCore = False
    group = None
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name
    if group == 'core_content_writter':
        isCore = True

    return render(request, 'website/create_post.html', {'form': form, 'isCore': isCore, 'allCategories': allCategories, 'allTags': allTags})

# Edit a post


@login_required
@notDeveloper()
def editPost(request, slug=None):
    item = get_object_or_404(BlogPost, slug=slug)
    # check for auth
    if item.user != request.user:
        return render(request, 'website/page-404.html')

    form = PostForm(request.POST or None, instance=item)
    if form.is_valid():
        # form.save()
        post_item = form.save(commit=False)
        post_item.user = request.user
        # status
        blogStatus = request.POST.get('status', None)
        # print(request.POST, blogStatus)
        if (blogStatus != None) and (blogStatus == 'ACTIVE'):
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
    return render(request, 'website/create_post.html', {'form': form, 'isCore': isCore})

# Delete a  Blog


@login_required
@notDeveloper()
def deletePost(request, slug):
    user = request.user
    # SomeModel.objects.filter(id=id).delete()
    BlogPost.objects.filter(slug=slug, user=user).delete()
    return redirect('dashboard')

# View Blogs


@login_required
@notDeveloper()
def viewBlogs(request):
    user = request.user
    allBlogs = BlogPost.objects.filter(
        status="ACTIVE", user=user).order_by('-pub_date')
    context = {
        'blogs': allBlogs
    }
    # print(allBlogs)
    return render(request, 'website/approved_blogs.html', context)

# Pending Blogs


@login_required
@notDeveloper()
def pendingBlogs(request):
    user = request.user
    allBlogs = BlogPost.objects.filter(
        status="PENDING", user=user).order_by('-pub_date')
    context = {
        'blogs': allBlogs
    }
    return render(request, 'website/pending_blogs.html', context)

# Developer Dashboard


@login_required
@onlyDeveloper()
def developerDashboard(request):
    return render(request, 'website/dashboard_admin.html')

# Developer pending post


@login_required
@onlyDeveloper()
def pendingBlogsDeveloper(request):
    allBlogs = BlogPost.objects.filter(status="PENDING").order_by('-pub_date')
    context = {
        'blogs': allBlogs
    }
    return render(request, 'website/pending_posts_developer.html', context)

# Developer pending post


@login_required
@onlyDeveloper()
def approvedBlogsDeveloper(request):
    allBlogs = BlogPost.objects.filter(status="ACTIVE").order_by('-pub_date')
    context = {
        'blogs': allBlogs
    }
    return render(request, 'website/approved_posts_developer.html', context)


@login_required
@onlyDeveloper()
def contactFormDeveloper(request):
    contactInfos = Contact.objects.all().order_by('-date')
    context = {'contactInfos': contactInfos}
    return render(request, 'website/contact_form_developer.html', context)

# Developer all post


@login_required
@onlyDeveloper()
def allBlogsDeveloper(request):
    allBlogs = BlogPost.objects.all().order_by('-pub_date')
    context = {
        'blogs': allBlogs
    }
    return render(request, 'website/all_posts_developer.html', context)

# Developer approve post


@login_required
@onlyDeveloper()
def approvePost(request, slug):
    try:
        blog = BlogPost.objects.get(slug=slug)
        blog.status = "ACTIVE"
        blog.save()
    except:
        pass
    return redirect('pending_blogs_developer')

# Developer pending post


@login_required
@onlyDeveloper()
def pendingPost(request, slug):
    try:
        blog = BlogPost.objects.get(slug=slug)
        blog.status = "PENDING"
        blog.save()
    except:
        pass
    return redirect('approved_blogs_developer')


# Developer delete post
@login_required
@onlyDeveloper()
def deletePostDeveloper(request, slug):
    try:
        BlogPost.objects.filter(slug=slug).delete()
    except:
        pass
    return redirect('pending_blogs_developer')

# preview a post


@login_required
@onlyDeveloper()
def previewPost(request, slug):
    try:
        blog = BlogPost.objects.get(slug=slug, status="PENDING")
        user = blog.user
    except:
        return redirect('pending_blogs_developer')
    context = {
        'blogpost': blog,
        'pub_user': user,
    }
    return render(request, 'website/single_preview.html', context)


@login_required
def comment(request, id):
    currentBlog = BlogPost.objects.get(id=id)
    comment = Comment(blog=currentBlog, author=Author.objects.get(user=request.user),
                      comment=request.POST.get('comment'))
    comment.save()
    return redirect('/news/'+str(currentBlog.slug))


def blogCatagory(request, catagory):
    recentPosts = BlogPost.objects.all().order_by('-pub_date')[:3]
    popularPosts = BlogPost.objects.all().order_by('-views')[:3]
    popularCatagories = Catagory.objects.filter(
        tranding=True).order_by('-date')
    popularCatagoriesDict = {}
    for i in popularCatagories:
        popularCatagoriesDict[i] = len(BlogPost.objects.filter(catagory=i))
    context = {'recentPosts': recentPosts, 'popularPosts': popularPosts,
               'popularCatagoriesDict': popularCatagoriesDict}

    try:
        thisCatagory = Catagory.objects.get(text=catagory)
    except:
        return render(request, 'website/page-404.html', context)
    blogs = BlogPost.objects.filter(
        catagory=thisCatagory).order_by('-pub_date')
    context['catagory'] = thisCatagory
    context['blogs'] = blogs
    return render(request, 'website/blog-category.html', context)

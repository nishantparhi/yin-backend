from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUserForm, PostForm, AuthorForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Contact, BlogPost, Catagory, Author, Comment, Tag
from .decorators import unauthentiated_user, notDeveloper, onlyDeveloper
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator


def index(request):
    trandingBlogs = BlogPost.objects.filter(
        isTranding=True).order_by('-pub_date')[:5]
    trandingCatagories = Catagory.objects.filter(
        tranding=True).order_by('-date')[:6]

    trandingCatagoriesPosts = []

    for i in trandingCatagories:
        trandingCatagoriesPosts.append(
            [i, BlogPost.objects.filter(catagory=i).filter(status="ACTIVE").order_by('-pub_date')])

    context = returnFooterDependencies()
    context['trandingPosts'] = trandingBlogs
    context['trendingPostContent'] = trandingCatagoriesPosts
    return render(request, 'website/index.html', context)


# def single(request, id):
#     blogs = BlogPost.objects.get(id=id)
#     # print(blogs)
#     context = {
#         'blogs': blogs,
#     }
#     return render(request, 'website/single.html', context)


def blogauthor(request, username):
    try:
        user = User.objects.get(username=username)
        # print(user)
        blogs = BlogPost.objects.filter(user=user).order_by('-pub_date')
        author = Author.objects.get(user=user)
    except:
        return render(request, 'website/page-404.html', returnFooterDependencies())
    # Paginatior
    p = Paginator(blogs, 5)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)

    context = returnFooterDependencies()
    context['blogs'] = page
    context['noOfPages'] = range(p.num_pages)
    context['author'] = author
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
    context = returnFooterDependencies()
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
        return render(request, 'website/page-404.html', returnFooterDependencies())

    # if blog is not active then don't show anyone
    if blogpost.status != 'ACTIVE':
        return render(request, 'website/page-404.html', returnFooterDependencies())

    # add view count
    blogpost.views = blogpost.views + 1
    blogpost.save()
    author = Author.objects.get(user=user)
    realatedPost = BlogPost.objects.filter(
        catagory=blogpost.catagory.first()).filter(status="ACTIVE").order_by('-pub_date')[:2]
    prevNextPost = BlogPost.objects.filter(
        user=blogpost.user).filter(status="ACTIVE").exclude(id=blogpost.id).order_by('-pub_date')[:2]
    print(prevNextPost[0].coverPic)
    comments = Comment.objects.filter(blog=blogpost)
    context = returnFooterDependencies()
    context['blogpost'] = blogpost
    context['author'] = author
    context['realatedPost'] = realatedPost
    context['prevNextPost'] = prevNextPost
    context['comments'] = comments
    return render(request, 'website/single.html', context)


# Create a new post
@login_required
@notDeveloper()
def createPost(request):
    user = request.user
    if request.method == "POST":
        # print(request.FILES)
        # print(request.FILES)
        # print(request.FILES)
        blogpost = BlogPost.objects.create(
            user=request.user,
            blog_title=request.POST.get('blog_title'),
            blog_content=request.POST.get('blog_content'),
            status=request.POST.get('status') or 'PENDING',
            coverPic=request.FILES.get('coverPic')


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
        return redirect('dashboard')

    selectedCats = []
    selectedtags = []
    allCategories = Catagory.objects.all()
    allTags = Tag.objects.all()
    tempCat = []
    for i in allCategories:
        if i in selectedCats:
            tempCat.append([i, True])
        else:
            tempCat.append([i, False])
    allCategories = tempCat
    tempCat = []
    for i in allTags:
        if i in selectedtags:
            tempCat.append([i, True])
        else:
            tempCat.append([i, False])
    allTags = tempCat
    form = PostForm()
    isCore = False
    group = None
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name
    if group == 'core_content_writter':
        isCore = True

    return render(request, 'website/create_post.html', {'form': form, 'isCore': isCore, 'allCategories': allCategories, 'allTags': allTags, 'item': None})

# Edit a post


@login_required
@notDeveloper()
def editPost(request, slug=None):
    item = get_object_or_404(BlogPost, slug=slug)
    # check for auth
    if item.user != request.user:
        return render(request, 'website/page-404.html',returnFooterDependencies())

    form = PostForm(request.POST or None, instance=item)
    if request.method == "POST":
        # print(request.POST.get('blog_title'))
        # print(request.POST.get('blog_title'))
        # print(request.POST.get('blog_title'))
        # print(request.FILES.get('coverPic'))

        item.blog_title = request.POST.get('blog_title')
        item.blog_content = request.POST.get('blog_content')
        item.status = request.POST.get('status') or 'PENDING'
        if(request.FILES.get('coverPic') != None):
            item.coverPic = request.FILES.get('coverPic')

        for i in item.catagory.all():
            item.catagory.remove(i.id)
        for i in item.tags.all():
            item.tags.remove(i.id)

        for id in request.POST.get('selectedCat').split(','):
            try:
                test = int(id)
                item.catagory.add(id)
            except:
                pass
        for id in request.POST.get('selectedTag').split(','):
            try:
                test = int(id)
                item.tags.add(id)
            except:
                pass
        item.save()

        return redirect('dashboard')

    # if the user is core member or not
    selectedCats = (item.catagory.all())
    selectedtags = (item.tags.all())
    allCategories = Catagory.objects.all()
    allTags = Tag.objects.all()
    tempCat = []
    for i in allCategories:
        if i in selectedCats:
            tempCat.append([i, True])
        else:
            tempCat.append([i, False])
    allCategories = tempCat
    tempCat = []
    for i in allTags:
        if i in selectedtags:
            tempCat.append([i, True])
        else:
            tempCat.append([i, False])
    allTags = tempCat

    isCore = False
    group = None
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name
    if group == 'core_content_writter':
        isCore = True
    # print(item.coverPic)
    return render(request, 'website/create_post.html', {'form': form, 'isCore': isCore, 'allCategories': allCategories, 'allTags': allTags, 'item': item})

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
    context = returnFooterDependencies()

    try:
        thisCatagory = Catagory.objects.get(text=catagory)
    except:
        return render(request, 'website/page-404.html', context)
    blogs = BlogPost.objects.filter(
        catagory=thisCatagory).order_by('-pub_date')
    # Paginatior
    p = Paginator(blogs, 5)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)

    context['catagory'] = thisCatagory
    context['blogs'] = page
    context['noOfPages'] = range(p.num_pages)
    return render(request, 'website/blog-category.html', context)

# User Roles
@login_required
@onlyDeveloper()
def userRoles(request):
    users = User.objects.all()
    userRoleDict = {}
    for user in users:
        userRoleDict[user] = user.groups.all()[0]

    context = {'userRoleDict': userRoleDict}
    return render(request, 'website/user_roles_developer.html', context)

# View a User
@login_required
@onlyDeveloper()
def viewUser(request, username):
    try:
        user = User.objects.get(username=username)
        role = user.groups.all()[0]
    except:
        return redirect('userRoles')

    if request.method == 'POST':
        userrole = request.POST.get('userrole')
        if userrole == 'developer' or userrole == 'core_content_writter' or userrole=='general_content_writer':
            # remove privious 
            user.groups.clear()
            # add new
            groupNew = Group.objects.get(name=userrole)
            user.groups.add(groupNew)
        return redirect('userRoles')

    

    context = {'user': user, 'role':role}
    return render(request, 'website/view_user_developer.html', context)

# Add Tag
@login_required
@onlyDeveloper()
def addTag(request):
    if request.method == 'POST':
        tag = request.POST.get('tag', None)
        if(not tag or tag.strip()==''):
            return redirect('addTag')
        Tag.objects.create(text=tag.strip())
    return render(request, 'website/add_Tag.html')

# Add Tag
@login_required
@onlyDeveloper()
def addCatagory(request):
    if request.method == 'POST':
        catagory = request.POST.get('catagory', None)
        trandingVal = request.POST.get('tranding', False)
        tranding = False
        if (trandingVal == 'on'):
            tranding = True
        if(not catagory or catagory.strip()==''):
            return redirect('addCatagory')
        print(catagory, tranding)
        Catagory.objects.create(text=catagory.strip(), tranding=tranding)
    return render(request, 'website/add_Catagory.html')

# Add Tag
@login_required
@onlyDeveloper()
def changeTranding(request, slug):
    try:
        blog = BlogPost.objects.get(slug=slug)
    except:    
        return redirect('approved_blogs_developer')
    blog.isTranding = not blog.isTranding
    blog.save()
    return redirect('approved_blogs_developer')

@login_required
@notDeveloper()
def myProfile(request):
    curr_author = Author.objects.get(user=request.user)
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=curr_author)
        if form.is_valid():
            form.save()
        # save the pic
        if(request.FILES.get('profilePic') != None):
            curr_author.profile_pic = request.FILES.get('profilePic')
            try:
                curr_author.save()
            except:
                pass
        return redirect('myProfile')

    role = request.user.groups.all()[0]
    form = AuthorForm(instance=curr_author)
    context = {'role': role, 'form': form}

    return render(request, 'website/my-profile.html', context)

def returnFooterDependencies():
    recentPosts = BlogPost.objects.all().order_by('-pub_date')[:3]
    popularPosts = BlogPost.objects.all().order_by('-views')[:3]
    popularCatagories = Catagory.objects.filter(
        tranding=True).order_by('-date')
    popularCatagoriesDict = {}
    for i in popularCatagories:
        popularCatagoriesDict[i] = len(BlogPost.objects.filter(catagory=i))
    # print(trandingCatagoriesPosts)
    context = {'recentPosts': recentPosts,
               'popularPosts': popularPosts,
               'popularCatagoriesDict': popularCatagoriesDict
               }
    return context
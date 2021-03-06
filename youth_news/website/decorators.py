from django.shortcuts import redirect, HttpResponse

def unauthentiated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)
    
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized to view this page.")
        return wrapper_func
    return decorator

def notDeveloper():
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            # print(group)
            if group == 'developer':
                # print("YES")
                return redirect('/developer')
            else:
                return view_func(request, *args, **kwargs)
        return wrapper_func
    return decorator

def onlyDeveloper():
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            # print(group)
            if group == 'developer':
                # print("YES")
                return view_func(request, *args, **kwargs)
            else:
                return redirect('/dashboard')
        return wrapper_func
    return decorator

'''
Group Name and Their Role
developer - can access/edit and approve any post and other settings
core_content_writter - can write and automatically approved
general_content_writer - can write but needs to approval of developer to publish blog.
'''
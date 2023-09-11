from django.shortcuts import render, redirect 
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from blog.models import Post
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.contrib import messages
from django.db.models import Count    

#request.POST['userb']
# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to login')
            return redirect('../login/')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html',{ 'form': form } )


def profile(request,username,tag_slug=None):

    us = User.objects.filter(username=username).first()
    object_list = Post.published.filter(author=us).all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 2) # 2 posts in each page
    page = request.GET.get('page')
    nop = Post.objects.filter(author=request.user).count()
    
    

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    context = {
        'posts':posts,
        'title':'Profile',
        'page':page,
        'tag':tag,
        'nop': nop
    }
    return render(request,'users/profile.html',context)

  







# Create your views here.

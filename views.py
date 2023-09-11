#...A Django view is just a Python function that receives a web request and returns a web response. All the logic to return the desired response goes inside the view...#
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post,Comment
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.views.generic import ListView,DetailView,CreateView
from django.core.mail import send_mail
from .forms import EmailPostForm,CommentForm,AddPostForm
from taggit.models import Tag
from django.db.models import Count
from blog.models import Post
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth.mixins import LoginRequiredMixin

Post.objects.filter(body__contains='framework')

def get_slug(pSlug):
    newstr = ''
    for a in pSlug:
        if (a != ' '):
            newstr = newstr + a
        else:
            newstr = newstr + '-'
    return (newstr)
 
# Create your views here.
def post_list(request):
    posts = Post.published.all()
    return render(request,'blog/post/list.html',{'posts': posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            
    else:
        comment_form = CommentForm()
    # List of similar post
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    return render(request,'blog/post/detail.html',{'post': post,'comments': comments,'new_comment': new_comment,'comment_form': comment_form,'similar_posts': similar_posts,})

def blogs(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 2) # 2 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    context = {
        'title':'Profile',
        'page':page,
        'tag':tag,
        'posts': posts
    }
    return render(request,'blog/blogs.html',context)
  

def aboutus(request):
    post = Post.published.all()
    return render(request,'blog/aboutus.html')


def addpost(request):
    form = AddPostForm(request.POST)
    if form.is_valid():
        pTitle = form.cleaned_data.get('title')
        pBody = form.cleaned_data.get('body')
        user = request.user 
        pSlug = get_slug(pTitle)
        post=Post(title=pTitle,body=pBody,slug=pSlug,author=request.user)
        post.save()
        return redirect(post)
        
    else:
        form = AddPostForm()
        
    context = {'form': form }
    return render(request,'blog/post.html', context)

def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 2 ) # 2 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/post/list.html',{'page': page,'posts': posts,'tag': tag})


def post_edit(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
    form = AddPostForm (request.POST)
    if form.is_valid():
        user = request.user 
        if post.author == user:
            nwTitle = form.cleaned_data.get('title')
            nwBody = form.cleaned_data.get('body')
            post.title=nwTitle
            post.body=nwBody
            pSlug = get_slug(nwTitle)
            post.slug = pSlug 
            post=Post(title=nwTitle,body=nwBody,slug=pSlug,author=request.user)
            post.save()
            return redirect(post)
    else:
        form = AddPostForm()     
    context = {'form': form, 'post':post}
    return render(request,'blog/post_edit.html', context)


def post_delete(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    user = request.user
    
    if user == post.author:
        post.delete()
        return redirect ('blog:blogs')
    else:
        messages.warning(request, 'You\'re not authorized to delete this post.')
        return redirect (post)

def post_deleted(request,year,month,day, post): 
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    post.delete()
    messages.success(request, f'Post successfully deleted!')
    return redirect('blog:blogs')
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog/post/list.html'

def post_share(request, post_id):
    # Retrieve post by id                         
    post = get_object_or_404(Post, id=post_id, status='published') 
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message,'admin@myblog.com',[cd['to']])
            sent = True 
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent}) 
    

    



        




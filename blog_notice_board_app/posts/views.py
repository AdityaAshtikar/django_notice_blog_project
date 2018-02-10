from django.utils.http import quote_plus
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages # FLASH MESSAGES
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
# Create your views here.
from posts.models import Post, Category
from posts.forms import PostForm
from django.utils import timezone

from django.contrib import auth
from django.contrib.auth.decorators import login_required

from django.urls import reverse
# for search feature
from django.db.models import Q

def all_categories(request):
    categories = Category.objects.all().order_by('topic')
    context = {"categories" : categories}
    return render(request, 'all_categories.html', context)

def post_create(request):
    if not request.user.is_authenticated():
        messages.error(request, "You need to login first")
        return redirect(reverse('posts:login'))
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully created a Notice")
        return HttpResponseRedirect(instance.get_absolute_url())

    # We can grab the title and content and save it manually using "Post.objects.create()" [no validation errors will pop up]
    # if request.method == 'POST':
    #     print("Content: " + request.POST.get('content'))
    #     print("Title: " + request.POST.get('title'))
    context = {
        "form": form
    }
    return render(request, "post_form.html", context)

def post_detail(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    if post.draft or post.publish_date > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(post.title)
    context = { "post": post,
                "share_string": share_string
                }
    return render(request, "post_detail.html", context)

def post_list(request):
    today = timezone.now().date()
    all_posts = Post.objects.active() #.order_by('-timestamp') - reverse ordering, done in Models
    if request.user.is_staff or request.user.is_superuser:
        all_posts = Post.objects.all().order_by('-updated').order_by('-timestamp')

    # Search Feature start

    query = request.GET.get("q")
    if query:
        all_posts = all_posts.filter(
                                    Q(title__icontains=query) |
                                    Q(content__icontains=query) |
                                    Q(user__first_name__icontains=query) |
                                    Q(user__last_name__icontains=query) |
                                    Q(timestamp__icontains=query)
                                )

    # end!

    paginator = Paginator(all_posts, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        "posts": posts,
        "title": "List of all the Notices",
        "today": today
    }
    return render(request, "post_list.html", context)

def post_update(request, slug=None):
    if not request.user.is_authenticated():
        messages.error(request, "You need to login first")
        return redirect(reverse('posts:login'))
    post = get_object_or_404(Post, slug=slug)
    if post.user.username == request.user.username:
        form = PostForm(request.POST or None, request.FILES or None, instance=post)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "Updated: %s" %(str(instance.updated)))
            messages.success(request, "Notice Successfully updated")
            return HttpResponseRedirect(instance.get_absolute_url())

        context = {
            "post": post,
            "form": form
        }
        return render(request, "post_form.html", context)
    else:
        messages.error(request, "You cannot edit this post!")
        return redirect(post.get_absolute_url())

def post_delete(request, slug=None):
    if not request.user.is_authenticated():
        messages.error(request, "You need to login first")
        return redirect(reverse('posts:login'))
    instance = get_object_or_404(Post, slug=slug)
    if instance.user.username == request.user.username:
        instance.delete()
        messages.success(request, "Successfully deleted a Notice")
        return redirect('posts:list')
    else:
        messages.error(request, "You cannot delete this notice!")
        return redirect(instance.get_absolute_url())

def login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect('posts:list')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect(reverse('posts:list'))
        else:
            messages.error(request, "Error Wrong username or password")

    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect(reverse('posts:list'))

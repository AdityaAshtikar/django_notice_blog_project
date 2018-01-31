from django.utils.http import quote_plus
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages # FLASH MESSAGES
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
# Create your views here.
from posts.models import Post
from posts.forms import PostForm
from django.utils import timezone

# for search feature
from django.db.models import Q

def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully created a Notice")
        return HttpResponseRedirect(instance.get_absolute_url())

    # We can grab the title and content and save it using manually using "Post.objects.create()" [no validation errors will pop up]
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
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    post = get_object_or_404(Post, slug=slug)
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

def post_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted a Notice")
    return redirect('posts:list')

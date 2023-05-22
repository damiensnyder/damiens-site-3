from django.http.response import Http404
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from random import random
from content.models import Tag, Content, Shortform


def front_page(request):
    posts = Content.objects.order_by('-timestamp')\
        .exclude(primary_tag=Tag.objects.get(url="meta"))
    if not is_friend(request):
        posts = posts.exclude(tags=Tag.objects.get(url="hidden"))
    tags_list = [{
        'url': "content",
        'name': "recent content",
        'featured_post': posts[0]
    }]
    add_most_recent_item(posts, tags_list, "blog", "blog posts")
    add_most_recent_item(posts, tags_list, "songs", "songs")
    add_most_recent_item(posts, tags_list, "videos", "videos")
    add_most_recent_item(posts, tags_list, "code", "code")
    notes = Shortform.objects.order_by('-timestamp')\
        .filter(primary_tag=Tag.objects.all().get(url="notes"))
    if notes.exists():
        last_note = notes[0]
        last_note.description = last_note.body
        tags_list.append({
            'url': "shortform",
            'name': "shortform",
            'featured_post': last_note
        })
    return render(request, 'content/front-page.html', {
        'tags': tags_list,
        'tag': {
            'name': "damien snyder" if random() < 0.95 else "damien spider"
        },
        'logged_in': request.user.is_authenticated
    })


def add_most_recent_item(posts, tags_list, tag_url, tag_name):
    filtered_posts = posts\
        .filter(primary_tag=Tag.objects.get(url=tag_url))\
        .exclude(id=tags_list[0]['featured_post'].id)
    if filtered_posts.exists():
        tags_list.append({
            'url': tag_url,
            'name': tag_name,
            'featured_post': filtered_posts[0]
        })


def all_content_menu(request, page_num=1):
    posts = Content.objects.all().order_by('-timestamp')\
        .exclude(primary_tag=Tag.objects.get(url="meta"))
    if not is_friend(request):
        posts = posts.exclude(tags=Tag.objects.get(url="hidden"))
    context = paginate(posts, page_num)
    context['tag'] = {
        'url': "content",
        'name': "content"
    }
    return render(request, 'content/all-content-menu.html', context)


def all_shortform_menu(request, page_num=1):
    posts = Shortform.objects.all().order_by('-timestamp')
    if not is_friend(request):
        posts = posts.exclude(primary_tag=Tag.objects.get(url="hidden"))
    context = paginate(posts, page_num)
    context['tag'] = {
        'url': "shortform",
        'name': "shortform"
    }
    return render(request, 'content/all-shortform-menu.html', context)


def tag_or_content(request, url, page_num=1):
    try:
        tag = Tag.objects.get(url=url)
        posts = Content.objects.filter(tags=tag)\
            .order_by('-timestamp')
        if not is_friend(request):
            posts = posts.exclude(tags=Tag.objects.get(url="hidden"))
        if not posts.exists():
            posts = Shortform.objects.filter(primary_tag=tag)\
                .order_by('-timestamp')
            if not is_friend(request):
                posts = posts.exclude(primary_tag=Tag.objects.get(url="hidden"))
            context = paginate(posts, page_num)
            context['tag'] = tag
            return render(request, 'content/shortform-tag.html', context) 
        context = paginate(posts, page_num)
        context['tag'] = tag
        return render(request, 'content/tag.html', context)
    except Tag.DoesNotExist:
        return content(request, None, url)


def content(request, tag_url, post_url):
    try:
        post = Content.objects.get(url=post_url)
        if (tag_url is not None) and (post.primary_tag.url != tag_url):
            raise Http404(f"No post found with tag \"{tag_url}\" and ID \"{post_url}\"")

        if post.tags.filter(url="hidden").exists() and not is_friend(request):
            return render(request, 'content/illegal-hidden-access.html', {
                'content': post
            })

        return render(request, 'content/content.html', {
            'content': post
        })
    except Content.DoesNotExist:
        try:
            post = Shortform.objects.get(url=post_url)
            if (tag_url is not None) and (post.primary_tag.url != tag_url):
                raise Http404(f"No post found with tag \"{tag_url}\" and ID \"{post_url}\"")
            if post.primary_tag == "hidden" and not is_friend(request):
                return render(request, 'content/illegal-hidden-access.html', {
                    'content': post
                })
            return render(request, 'content/shortform.html', {
                'content': post
            })
        except Shortform.DoesNotExist:
            raise Http404(f"No content found with ID \"{post_url}\"")


def is_friend(request):
    return request.user.groups.filter(name="friends").exists()


def paginate(posts, page_num):
    num_posts = len(posts)
    num_pages = int((num_posts + 19) / 20)
    if page_num > num_pages:
        page_num = num_pages
    if page_num < 1:
        page_num = 1
    return {
        'posts': posts[20 * (page_num - 1):20 * page_num],
        'page_num': page_num,
        'num_pages': num_pages
    }


def signup(request):
    if request.user.is_authenticated:
        return redirect('/profile')
    elif request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'content/signup.html', {
        'form': form,
        'tag': {'name': "make an account"}
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/profile')
    elif request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('/profile')
    form = AuthenticationForm()
    return render(request, 'content/login.html', {
        'form': form,
        'tag': {'name': "log in"}
    })


def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    else:
        logout(request)
        return redirect('/')


def profile(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    else:
        return render(request, 'content/profile.html', {
            'form': request.user
        })
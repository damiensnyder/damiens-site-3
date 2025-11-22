from django.http.response import Http404
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from random import random
from content.models import Tag, Content, Shortform, Message
from content.forms import ChangeSettingsForm, MessageForm
import datetime
from accounts.models import User
from accounts.forms import CreateUser
from django.db.models import Q


def front_page(request):
    posts = Content.objects.order_by('-timestamp')
    posts = remove_hidden(posts, request)
    featured_post = {
        'url': "content",
        'name': "more posts",
        'post': posts[0]
    }
    last_note = Shortform.objects.order_by('-timestamp')\
        .filter(primary_tag=Tag.objects.all().get(url="notes"))[0]
    last_note.description = last_note.body
    last_note.thumbnail = "thumbs/notes.jpg"
    featured_note = {
        'url': "shortform",
        'name': "shortform",
        'post': last_note
    }
    return render(request, 'content/front-page.html', {
        'featured_post': featured_post,
        'featured_note': featured_note,
        'tag': {
            'name': "damien snyder" if random() < 0.95 else "damien spider"
        },
        'logged_in': request.user.is_authenticated,
        'theme': get_theme(request)
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
    posts = Content.objects.all().order_by('-timestamp')
    posts = remove_hidden(posts, request)
    context = paginate(posts, page_num)
    context['tag'] = {
        'url': "content",
        'name': "content"
    }
    context['theme'] = get_theme(request)
    return render(request, 'content/all-content-menu.html', context)


def all_shortform_menu(request, page_num=1):
    posts = Shortform.objects.all().order_by('-timestamp')
    posts = remove_hidden(posts, request)
    context = paginate(posts, page_num)
    context['tag'] = {
        'url': "shortform",
        'name': "shortform"
    }
    context['theme'] = get_theme(request)
    return render(request, 'content/all-shortform-menu.html', context)


def tag_or_content(request, url, page_num=1):
    try:
        tag = Tag.objects.get(url=url)
        posts = Content.objects.filter(tags=tag)\
            .order_by('-timestamp')
        posts = remove_hidden(posts, request)
        if not posts.exists():
            posts = Shortform.objects.filter(primary_tag=tag)\
                .order_by('-timestamp')
            posts = remove_hidden(posts, request)
            context = paginate(posts, page_num)
            context['tag'] = tag
            context['theme'] = get_theme(request)
            return render(request, 'content/shortform-tag.html', context) 
        context = paginate(posts, page_num)
        context['tag'] = tag
        context['theme'] = get_theme(request)
        return render(request, 'content/tag.html', context)
    except Tag.DoesNotExist:
        return content(request, None, url)


def remove_hidden(posts, request):
    if request.user.is_authenticated:
        return posts.filter(Q(group_needed=None) | Q(group_needed__in=request.user.groups.all()))
    else:
        return posts.filter(group_needed=None)


def content(request, tag_url, post_url):
    try:
        post = Content.objects.get(url=post_url)
        if (tag_url is not None) and (post.primary_tag.url != tag_url):
            raise Http404(f"No post found with tag \"{tag_url}\" and ID \"{post_url}\"")

        if not can_access(post, request):
            return render(request, 'content/illegal-hidden-access.html', {
                'content': post,
                'theme': get_theme(request)
            })

        return render(request, 'content/content.html', {
            'content': post,
            'form': MessageForm(),
            'theme': get_theme(request)
        })
    except Content.DoesNotExist:
        try:
            post = Shortform.objects.get(url=post_url)
            if (tag_url is not None) and (post.primary_tag.url != tag_url):
                raise Http404(f"No post found with tag \"{tag_url}\" and ID \"{post_url}\"")
            if not can_access(post, request):
                return render(request, 'content/illegal-hidden-access.html', {
                    'content': post,
                    'theme': get_theme(request)
                })
            return render(request, 'content/shortform.html', {
                'content': post,
                'form': MessageForm(),
                'theme': get_theme(request)
            })
        except Shortform.DoesNotExist:
            raise Http404(f"No content found with ID \"{post_url}\"")


def can_access(post, request):
    return post.group_needed is None or \
        (request.user.is_authenticated and (post.group_needed in request.user.groups.all()))


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


def signup(request, dest_tag=None, dest_post=None):
    if request.user.is_authenticated:
        return redirect('/profile')
    elif request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            if dest_tag is not None and dest_post is not None:
                return redirect(f'/{dest_tag}/{dest_post}')
            return redirect('/')
    else:
        form = CreateUser()
    return render(request, 'content/signup.html', {
        'form': form,
        'tag': {'name': "make an account"},
        'theme': get_theme(request)
    })


def login_view(request, dest_tag=None, dest_post=None):
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
                if dest_tag is not None and dest_post is not None:
                    return redirect(f'/{dest_tag}/{dest_post}')
                return redirect('/profile')
    form = AuthenticationForm()
    return render(request, 'content/login.html', {
        'form': form,
        'tag': {'name': "log in"},
        'theme': get_theme(request)
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
            'user': request.user,
            'form': ChangeSettingsForm(initial={
                'email': request.user.email,
                'theme': request.user.theme
            }),
            'theme': get_theme(request)
        })
    

def send_message(request, tag_url, post_url):
    if request.method == "POST":
        try:
            post = Content.objects.get(url=post_url)
            was_content = True
        except Content.DoesNotExist:
            try:
                post = Shortform.objects.get(url=post_url)
                was_content = False
            except Shortform.DoesNotExist:
                raise Http404(f"No post found with URL {post_url}")
        form = MessageForm(data=request.POST)
        if form.is_valid():
            user = None
            if (not form.cleaned_data.get('anonymous')) and request.user.is_authenticated:
                user = request.user
            message = Message(
                timestamp=datetime.datetime.now(),
                body=form.cleaned_data.get('body'),
                from_content=post if was_content else None,
                from_shortform=None if was_content else post,
                user=user
            )
            message.save()
        # return content(request, tag_url, post_url)  [gets URL wrong]
        return redirect(f"/{tag_url}/{post_url}/")


def change_settings(request):
    if request.method == "POST":
        form = ChangeSettingsForm(data=request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                user = request.user
            else:
                return redirect(f"/login/")
            user.theme = form.cleaned_data.get('theme')
            user.email = form.cleaned_data.get('email')
            user.save()
            return redirect(f"/profile/")
    return redirect(f"/profile/")


def upload_file(request):
    pass


def get_theme(request):
    if request.user.is_authenticated:
        return request.user.theme
    return "auto"


def theme_preview(request):
    """Theme preview page for testing all available themes"""
    # Get theme from query parameter or default to auto
    preview_theme = request.GET.get('theme', 'auto')

    # All available themes
    themes = [
        ('auto', 'Auto'),
        ('light_mode', 'Light Mode'),
        ('dark_mode', 'Dark Mode'),
        ('forest', 'Forest'),
        ('hacker', 'Hacker'),
        ('vice', 'Vice'),
        ('suffering', 'Suffering'),
        ('unstyled', 'Unstyled HTML'),
        ('dignified', 'Dignified'),
        ('geocities', 'Geocities'),
        ('geocities_extreme', 'Geocities EXTREME'),
        ('cyberpunk', 'Cyberpunk'),
        ('fantasy', 'Fantasy'),
        ('whimsy', 'Whimsy'),
        ('seapunk', 'Seapunk'),
        ('modern_light', 'Modern Light'),
        ('modern_dark', 'Modern Dark'),
        ('helvetica_light', 'Helvetica Light'),
        ('helvetica_dark', 'Helvetica Dark'),
        ('low_contrast', 'Low Contrast'),
        ('terminal', 'Terminal'),
        ('sunset', 'Sunset'),
        ('ocean', 'Ocean'),
        ('chocolate', 'Chocolate'),
        ('neon', 'Neon'),
        ('high_contrast', 'High Contrast'),
        ('solarized', 'Solarized'),
    ]

    return render(request, 'content/theme-preview.html', {
        'theme': preview_theme,
        'themes': themes,
        'current_theme': preview_theme,
        'tag': {'name': 'Theme Preview'},
        'logged_in': request.user.is_authenticated,
    })
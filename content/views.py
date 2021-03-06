from django.http.response import Http404
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from random import random
from content.models import Tag, Content, Shortform


def front_page(request):
    posts = Content.objects.order_by('-timestamp')\
        .exclude(primary_tag="meta")
    if not is_friend(request):
        posts = posts.exclude(tags="hidden")
    tags_list = [{
        'id': "content",
        'name': "recent content",
        'featured_post': posts[0]
    }]
    add_most_recent_item(posts, tags_list, "blog", "blog posts")
    add_most_recent_item(posts, tags_list, "songs", "songs")
    add_most_recent_item(posts, tags_list, "videos", "videos")
    add_most_recent_item(posts, tags_list, "code", "code")
    notes = Shortform.objects.order_by('-timestamp')\
        .filter(primary_tag="notes")
    if notes.exists():
        last_note = notes[0]
        last_note.description = last_note.body
        tags_list.append({
            'id': "shortform",
            'name': "shortform",
            'featured_post': last_note
        })
    return render(request, 'content/front-page.html', {
        'tags': tags_list,
        'tag': {
            'name': "damien snyder" if random() < 0.95 else "damien spider"
        }
    })


def add_most_recent_item(posts, tags_list, tag_id, tag_name):
    filtered_posts = posts\
        .filter(primary_tag=tag_id)\
        .exclude(id=tags_list[0]['featured_post'].id)
    if filtered_posts.exists():
        tags_list.append({
            'id': tag_id,
            'name': tag_name,
            'featured_post': filtered_posts[0]
        })


def all_content_menu(request, page_num=1):
    posts = Content.objects.all().order_by('-timestamp')\
        .exclude(primary_tag="meta")
    if not is_friend(request):
        posts = posts.exclude(tags="hidden")
    context = paginate(posts, page_num)
    context['tag'] = {
        'id': "content",
        'name': "content"
    }
    return render(request, 'content/all-content-menu.html', context)


def all_shortform_menu(request, page_num=1):
    posts = Shortform.objects.all().order_by('-timestamp')
    if not is_friend(request):
        posts = posts.exclude(primary_tag="hidden")
    context = paginate(posts, page_num)
    context['tag'] = {
        'id': "shortform",
        'name': "shortform"
    }
    return render(request, 'content/all-shortform-menu.html', context)


def tag_or_content(request, id, page_num=1):
    try:
        tag = Tag.objects.get(pk=id)
        posts = Content.objects.filter(tags=tag.id)\
            .order_by('-timestamp')
        if not is_friend(request):
            posts = posts.exclude(tags="hidden")
        if not posts.exists():
            posts = Shortform.objects.filter(primary_tag=tag.id)\
                .order_by('-timestamp')
            if not is_friend(request):
                posts = posts.exclude(primary_tag="hidden")
            context = paginate(posts, page_num)
            context['tag'] = tag
            return render(request, 'content/shortform-tag.html', context) 
        context = paginate(posts, page_num)
        context['tag'] = tag
        return render(request, 'content/tag.html', context)
    except Tag.DoesNotExist:
        return content(request, None, id)


def content(request, tag, id):
    try:
        post = Content.objects.get(pk=id)
        if (tag is not None) and (post.primary_tag.id != tag):
            raise Http404(f"No post found with tag \"{tag}\" and id \"{id}\"")

        if post.tags.filter(id="hidden").exists() and not is_friend(request):
            return render(request, 'content/illegal-hidden-access.html', {
                'content': post
            })

        return render(request, 'content/content.html', {
            'content': post
        })
    except Content.DoesNotExist:
        try:
            post = Shortform.objects.get(pk=id)
            if (tag is not None) and (post.primary_tag.id != tag):
                raise Http404(f"No post found with tag \"{tag}\" and id \"{id}\"")
            if post.primary_tag == "hidden" and not is_friend(request):
                return render(request, 'content/illegal-hidden-access.html', {
                    'content': post
                })
            return render(request, 'content/shortform.html', {
                'content': post
            })
        except Shortform.DoesNotExist:
            raise Http404(f"No content found with id \"{id}\"")


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
    if request.method == 'POST':
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
from django.http.response import Http404
from django.shortcuts import render
from django.http import HttpResponse

from content.models import Tag, Content, Shortform


def front_page(request):
    posts = Content.objects.order_by('-timestamp')\
        .exclude(primary_tag="meta")
    if not is_friend(request):
        posts = posts.exclude(tags="hidden")
    tags = [{
        'id': "content",
        'name': "recent content",
        'featured_post': posts[0]
    }]
    tags.append({
        'id': "blog",
        'name': "blog posts",
        'featured_post': posts\
            .filter(primary_tag="blog")\
            .exclude(id=tags[0]['featured_post'].id)[0]
    })
    tags.append({
        'id': "songs",
        'name': "songs",
        'featured_post': posts\
            .filter(primary_tag="songs")\
            .exclude(id=tags[0]['featured_post'].id)[0]
    })
    tags.append({
        'id': "videos",
        'name': "videos",
        'featured_post': posts\
            .filter(primary_tag="videos")\
            .exclude(id=tags[0]['featured_post'].id)[0]
    })
    last_note = Shortform.objects.order_by('-timestamp')\
        .filter(primary_tag="notes")\
        .exclude(id=tags[0]['featured_post'].id)[0]
    last_note.description = last_note.body
    tags.append({
        'id': "shortform",
        'name': "shortform",
        'featured_post': last_note
    })
    return render(request, 'content/front-page.html', {
        'tags': tags
    })


def all_content_menu(request):
    posts = Content.objects.all().order_by('-timestamp')\
        .exclude(primary_tag="meta")
    if not is_friend(request):
        posts = posts.exclude(tags="hidden")
    return render(request, 'content/all-content-menu.html', {
        'posts': posts
    })


def all_shortform_menu(request):
    posts = Shortform.objects.all().order_by('-timestamp')
    if not is_friend(request):
        posts = posts.exclude(tags="hidden")
    return render(request, 'content/all-shortform-menu.html', {
        'posts': posts
    })


def tag_or_content(request, id):
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
                posts = posts.exclude(tags="hidden")
            return render(request, 'content/shortform-tag.html', {
                'tag': tag,
                'posts': posts
            })
        return render(request, 'content/tag.html', {
            'tag': tag,
            'posts': posts
        })
    except Tag.DoesNotExist:
        return content(request, None, id)


def content(request, tag, id):
    try:
        post = Content.objects.get(pk=id)
        if (tag is not None) and (post.primary_tag.id != tag):
            raise Http404(f"No post found with tag \"{tag}\" and id \"{id}\"")

        if post.tags.filter(id="hidden").exists() and not is_friend(request):
            return render(request, 'content/illegal_hidden_access.html', {
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
            if post.tags.filter(id="hidden").exists() and not is_friend(request):
                return render(request, 'content/illegal_hidden_access.html', {
                    'content': post
                })
            return render(request, 'content/shortform.html', {
                'content': post
            })
        except Shortform.DoesNotExist:
            raise Http404(f"No content found with id \"{id}\"")


def is_friend(request):
    return request.user.groups.filter(name="friends").exists()

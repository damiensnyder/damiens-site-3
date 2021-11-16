from django.http.response import Http404
from django.shortcuts import render
from django.http import HttpResponse

from content.models import Tag, Content


def front_page(request):
    non_shortform = Content.objects.filter(is_shortform=False)\
                                   .order_by('-timestamp')
    tags = [{
        'id': "content",
        'name': "recent content",
        'featured_post': non_shortform[0]
    }]
    tags.append({
        'id': "blog",
        'name': "blog posts",
        'featured_post': non_shortform\
            .filter(primary_tag="blog")\
            .exclude(id=tags[0]['featured_post'].id)[0]
    })
    tags.append({
        'id': "songs",
        'name': "songs",
        'featured_post': non_shortform\
            .filter(primary_tag="songs")\
            .exclude(id=tags[0]['featured_post'].id)[0]
    })
    tags.append({
        'id': "videos",
        'name': "videos",
        'featured_post': non_shortform\
            .filter(primary_tag="videos")\
            .exclude(id=tags[0]['featured_post'].id)[0]
    })
    return render(request, 'content/front-page.html', {
        'tags': tags
    })


def all_content_menu(request):
    posts = Content.objects.all().order_by('-timestamp')
    return render(request, 'content/all-content-menu.html', {
        'posts': posts
    })


def tag_or_content(request, id):
    try:
        tag = Tag.objects.get(pk=id)
        posts = Content.objects.filter(tags=tag.id)\
                               .order_by('-timestamp')
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
        return render(request, 'content/content.html', {
            'content': post
        })
    except Content.DoesNotExist:
        raise Http404(f"No content found with tag \"{tag}\"")

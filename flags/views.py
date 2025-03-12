import uuid
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.db.models import F
import random
from content.views import get_theme
from .models import Flag, Pin, Report, Vote


@require_http_methods(["GET", "POST"])
def vote(request):
    """
    View for displaying 8 random flags and handling votes.
    GET: Display the flags
    POST: Process the vote submission
    """
    
    # Handle form submission
    if request.method == "POST":
        selected_flags = request.POST.getlist('selected_flags')
        all_options = request.POST.getlist('all_flags')
        selected_flags = [int(flag) for flag in selected_flags]
        unselected_flags = [int(flag) for flag in all_options if int(flag) not in selected_flags]
        selected_flags = Flag.objects.filter(pk__in=selected_flags)
        unselected_flags = Flag.objects.filter(pk__in=unselected_flags)

        # Create a new vote
        matchup_id = uuid.uuid4()
        for flag in selected_flags:
            vote = Vote(
                matchup_id=matchup_id,
                user=request.user if request.user.is_authenticated else None,
                flag=flag,
                score=len(unselected_flags) + 5
            )
            vote.save()
            flag.num_votes += 1
            flag.total_score += len(unselected_flags) + 5
            flag.save()
        for flag in unselected_flags:
            vote = Vote(
                matchup_id=matchup_id,
                user=request.user if request.user.is_authenticated else None,
                flag=flag,
                score=-len(selected_flags) - 5
            )
            vote.save()
            flag.num_votes += 1
            flag.total_score -= len(selected_flags) - 5
            flag.save()

        # Redirect to the same page to prevent form resubmission
        return redirect("flags:vote")
    
    # Prepare context for template rendering
    all_flags = list(Flag.objects.all())
    
    # Filter out flags with height greater than their width
    all_flags = [flag for flag in all_flags if flag.height <= flag.width]
    selected_flags = random.sample(all_flags, 6)

    # Constrain to max-height 200 max-width 350 while maintaining aspect ratio
    for flag in selected_flags:
        if flag.height > 180:
            flag.width = int(flag.width * 180 / flag.height)
            flag.height = 180
        if flag.width > 300:
            flag.height = int(flag.height * 300 / flag.width)
            flag.width = 300
    
    context = {
        'flags': selected_flags,
        'theme': get_theme(request)
    }
    
    return render(request, 'flags/vote.html', context)


def leaderboard(request):
    """
    View for displaying the leaderboard of flags based on votes.
    """
    # Get the top 10 flags based on the score field
    # Filter out flags with height greater than width
    top_flags = Flag.objects.filter(height__lte=F('width')).order_by(F('leaderboard_score').desc())[:100]

    for flag in top_flags:
        if flag.height > 180:
            flag.width = int(flag.width * 180 / flag.height)
            flag.height = 180
        if flag.width > 300:
            flag.height = int(flag.height * 300 / flag.width)
            flag.width = 300
    
    context = {
        'flags': top_flags,
        'theme': get_theme(request)
    }
    
    return render(request, 'flags/leaderboard.html', context)


@login_required(login_url='login')
def favorites(request, page_num=1):
    """
    View for displaying the flags that the user has pinned or voted in favor of.
    """
    # Get the flags that the user has pinned
    pinned_flags = Flag.objects.filter(pin__user=request.user).distinct()
    liked_flags = Flag.objects.filter(vote__user=request.user, vote__score__gt=0).distinct()

    # Constrain flags to 300x180
    for flag in pinned_flags.union(liked_flags):
        if flag.height > 180:
            flag.width = int(flag.width * 180 / flag.height)
            flag.height = 180
        if flag.width > 300:
            flag.height = int(flag.height * 300 / flag.width)
            flag.width = 300

    # Paginate liked_flags by 100s
    num_pages = (len(pinned_flags) + len(liked_flags) + 99) // 100
    liked_flags = liked_flags[(page_num - 1) * 100:page_num * 100]
    
    context = {
        'pinned_flags': pinned_flags,
        'liked_flags': liked_flags,
        'page_num': page_num,
        'num_pages': num_pages,
        'user': request.user,
        'theme': get_theme(request)
    }
    
    return render(request, 'flags/favorites.html', context)


def flag_info(request, flag_id):
    """
    View for displaying information about a specific flag.
    """
    try:
        flag = Flag.objects.get(pk=flag_id)
    except Flag.DoesNotExist:
        return redirect('flags:leaderboard')
    context = {
        'flag': flag,
        'theme': get_theme(request),
        'user': request.user
    }
    
    return render(request, 'flags/flag-info.html', context)


@permission_required('flags.delete_flag')
def reported_flags(request):
    # select all flags that have an associated Report object
    reported_flags = Flag.objects.filter(report__isnull=False).distinct()
    context = {
        'reported_flags': reported_flags,
        'theme': get_theme(request)
    }
    return render(request, 'flags/reported-flags.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def pin_flag(request):
    flag_id = json.loads(request.body)['flag_id']
    Pin.objects.create(
        flag=Flag.objects.get(pk=flag_id),
        user=request.user
    )
    return JsonResponse({'status': 200})


@login_required(login_url='login')
@require_http_methods(["POST"])
def unpin_flag(request):
    flag_id = json.loads(request.body)['flag_id']
    Pin.objects.get(flag=Flag.objects.get(pk=flag_id), user=request.user).delete()
    return JsonResponse({'status': 200})


@require_http_methods(["POST"])
def report_flag(request):
    flag_id = json.loads(request.body)['flag_id']
    Report.objects.create(
        flag=Flag.objects.get(pk=flag_id),
        user=request.user
    )
    return JsonResponse({'status': 200})


@permission_required('flags.delete_flag')
@require_http_methods(["POST"])
def delete_flag(request):
    flag_id = json.loads(request.body)['flag_id']
    Flag.objects.get(pk=flag_id).delete()
    return JsonResponse({'status': 200})

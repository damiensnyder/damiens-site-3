import uuid
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db.models import F
import random
from content.views import get_theme
from .models import Flag, Vote


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
                score=len(unselected_flags)
            )
            vote.save()
            flag.num_votes += 1
            flag.total_score += len(unselected_flags)
            flag.save()
        for flag in unselected_flags:
            vote = Vote(
                matchup_id=matchup_id,
                user=request.user if request.user.is_authenticated else None,
                flag=flag,
                score=-len(selected_flags)
            )
            vote.save()
            flag.num_votes += 1
            flag.total_score -= len(selected_flags)
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
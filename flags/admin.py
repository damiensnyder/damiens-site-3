from django.contrib import admin
from .models import Flag, Vote


class FlagAdmin(admin.ModelAdmin):
    list_display = ('name', 'img_url', 'width', 'height', 'source', 'total_score', 'num_votes')
    list_filter = ('num_votes', 'total_score')
    search_fields = ('name__icontains',)


class VoteAdmin(admin.ModelAdmin):
    list_display = ('matchup_id', 'flag', 'user', 'score')
    list_filter = ('score',)
    search_fields = ('flag__name__icontains', 'user__username__icontains')


admin.site.register(Flag, FlagAdmin)
admin.site.register(Vote, VoteAdmin)
